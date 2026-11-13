<!-- GENERATED copy of skills/mongo-index-review/SKILL.md. Do not edit here. -->

> Bundled copy of the `mongo-index-review` skill. Its skill directory (`<skill-dir>`, "this
> skill's folder") is the folder holding this guide, `references/mongo-index-review/` inside
> the bundle, so `scripts/`, `references/`, `examples/`, and `agents/` paths resolve from here.

# Mongo index review

Find every query a scope issues, decide which index serves it, and report the
indexes to add, change, or drop. This skill only diagnoses. Schema changes go
through `mongoose-schema-safety` (it owns index rollout).

Done when the report below lists every query shape in scope with its serving
index (existing or recommended), and every recommendation names the code that
needs it.

## 1. Pick the scope

| Request | Scope | How to list files |
| --- | --- | --- |
| PR / branch | Queries added or changed by the diff, plus the models they hit | `git diff --name-only origin/master...HEAD`; for a PR number `gh pr diff <n> --name-only` |
| One API | One model, its `modelRouter`, actions, hooks, and every other caller of the model | `grep -rn "<ModelName>\." --include=*.ts` outside tests |
| Whole package | Every model and every query in the package | All `*.ts` under the package `src/`, excluding `*.test.ts` |

For a PR, still read the full model schema and existing indexes: a new query is
judged against what is already there. Skip test files, seeds, and one-off
migration scripts unless the user asks; note them as excluded.

## 2. Inventory existing indexes

Framework paths below are relative to the `@terreno/api` package: `api/src/…`
in the Terreno monorepo, `node_modules/@terreno/api/dist/…` (`.js`) in an app.

For each model in scope, record every index:

- `schema.index({...}, {...})` calls, including options (`unique`, `sparse`,
  `partialFilterExpression`, `expireAfterSeconds`, `collation`).
- Field-level `index: true`, `unique: true`, `sparse: true`.
- Indexes added by plugins. In `@terreno/api`: `createdUpdatedPlugin` indexes
  `created` and `updated`; `isDeletedPlugin` indexes `deleted`;
  `isDisabledPlugin` indexes `disabled`; `excludeArchivedPlugin` indexes
  `archived`; `baseUserPlugin` indexes `email`; `firebaseJWTPlugin` indexes
  `firebaseId`; the sync plugin indexes `_syncSeq`. Check the plugin source (`plugins.ts`) for the
  current list rather than trusting this one.
- Indexes created at runtime. Registering a `modelRouter` with `sync` creates
  `{<scopeField>: 1, _syncSeq: 1}` (or `{_syncSeq: 1}` without a scope) in
  `sync/registrationSideEffects.ts`. Do not recommend duplicates.

Note `autoIndex` settings: when it is off in production, schema indexes exist
only if something builds them. Flag models whose indexes nothing creates.

## 3. Inventory query shapes

A query shape is: filter fields with operator class (equality, range, `$in`,
`$ne`/`$nin`, `$regex`, `$exists`, `$or`), sort fields with direction, and
whether it counts, skips, or projects. Collect shapes from:

**`modelRouter` list (most traffic, easiest to miss).** The list query is the
merge (`api.ts`) of `queryFilter(user, query)`, `defaultQueryParams`, client params allowed
by `queryFields`, `deleted: {$ne: true}` from `isDeletedPlugin`, and
`archived: {$ne: true}` from `excludeArchivedPlugin` when the model uses it. It sorts by
`sort` (or a client `?sort=` limited to `queryFields`, `sort`, and
`sortFields`), runs `countDocuments` on the same filter for `total`, and pages
with `skip`. So each list route yields:

- the base shape: `queryFilter` fields + `deleted`/`archived` + default sort;
- one shape per realistic client filter from `queryFields` (read the frontend
  callers — `useQuery`/`useGetXQuery` args, admin table filters — to see which
  combinations are actually sent);
- one shape per allowed client sort.

**Other framework paths.** `read`/`update`/`delete` and `IsOwner` use `_id`
(free). `populatePaths` resolves by `_id` (free). Admin routes (`AdminApp`)
list with `listFields` filters and `defaultSort` (default `-created`). Sync
snapshot/catch-up uses the runtime sync index.

**Hand-written queries.** `find`, `findExactlyOne`, `findOneOrNone`,
`findOneOrThrow`, `countDocuments`, `exists`, `distinct`, `updateMany`,
`deleteMany`, `findOneAndUpdate`, `aggregate`, and `bulkWrite` filters in
`collectionActions`, `instanceActions`, `pre*`/`post*` hooks, schema
middleware, statics/methods, services, jobs (`@terreno/jobs`), scripts, and
socket handlers. For `aggregate`, the leading `$match` + `$sort` use indexes;
`$lookup` needs an index on the foreign `foreignField`.

Record each shape once with every call site (`file:line`) that issues it and a
traffic guess: per request, per list page, per job run, admin-only, one-off.

## 4. Match shapes to indexes

For each shape, decide whether an existing index serves it, using these rules:

- **ESR order.** Compound key order is Equality fields, then Sort fields, then
  Range fields. A sort that cannot use the index forces an in-memory sort
  (spills to disk or fails on large results, and is slow well before that).
- **Prefix rule.** `{a, b, c}` serves queries on `a`, `a+b`, `a+b+c`. It makes a
  standalone `{a}` index redundant.
- **Sort direction.** A compound index serves its sort and the exact reverse of
  it; mixed directions must match the index (`{a: 1, b: -1}` serves
  `a asc, b desc` and `a desc, b asc` only).
- **`deleted: {$ne: true}` / `archived: {$ne: true}`.** Not selective and treated as a range. Put
  the field after equality and sort keys, or leave it out when such rows are
  rare. Never recommend `{deleted: 1}` or `{archived: 1}` alone as a fix. If most documents are
  soft-deleted, a `partialFilterExpression: {deleted: false}` index is
  appropriate only when every query on that path also filters `deleted: false`
  (a `$ne: true` filter does not match a partial index).
- **`$or`.** Each branch needs its own usable index or the query scans.
- **`$in`.** Acts as equality for key order, but combined with a sort it can
  force an in-memory sort when the list is long; note it.
- **`$regex`.** Only an anchored, case-sensitive prefix (`^abc`) uses an index.
  Case-insensitive search needs a collation index or a normalized field; free
  text needs Atlas Search or a text index. Recommend a rewrite, not an index.
- **Arrays.** Indexes on array fields are multikey; a compound index may hold
  at most one array field.
- **`countDocuments` + `skip`.** Both scan every matching key. On large
  collections, a covering index helps, but deep `skip` pagination stays linear;
  recommend cursor (range on the sort key) pagination when pages go deep.
- **Uniqueness.** A `findExactlyOne`/`findOneOrNone` lookup on a natural key
  (email, externalId, slug) should be backed by a `unique` index, or a
  `partialFilterExpression` unique index when the field is optional.
- **Expiry.** Collections that grow forever (logs, events, tokens) where code
  deletes by age should use a TTL index instead of a cron `deleteMany`.
- **Tenancy.** In multi-tenant or owner-scoped apps the scope field
  (`ownerId`, `organizationId`, `carePod`, …) almost always leads the compound.

Each index costs write time and RAM. Prefer one compound index that serves
several shapes over several narrow ones. Do not recommend an index for a shape
that runs only in admin tools on a small collection, unless the user asks.

## 5. Verify when a database is available (optional)

Static analysis is the default. When the user points at a non-production
database (local, test, staging), confirm the top findings:

```js
db.<collection>.find(<filter>).sort(<sort>).explain("executionStats")
// Look for COLLSCAN, SORT (in-memory), and totalKeysExamined >> nReturned.
db.<collection>.aggregate([{$indexStats: {}}])  // accesses.ops == 0 → unused candidate
db.<collection>.getIndexes()
```

Never read documents from a production or PHI-bearing database for this
review; `explain`, `getIndexes`, `$indexStats`, and `collStats` return metadata
only. Ask before connecting to any shared database.

## 6. Report

Lead with the highest-impact addition. Keep each recommendation tied to code.

```markdown
## Mongo index review: <scope> (<n> models, <m> query shapes)

### Add
1. `todoSchema.index({ownerId: 1, completed: 1, created: -1})` — Todo
   - Serves: list `GET /todos?completed=` (`example-backend/src/api/todos.ts:40`),
     `bulkComplete` (`…/todos.ts:88`)
   - Why: equality `ownerId`, `completed`; sort `-created`; today scans all of
     the owner's todos and sorts in memory
   - Confidence: High | Medium | Low (Low = depends on data distribution you
     could not see)

### Change
- Replace `{ownerId: 1}` with the compound above (prefix makes it redundant)

### Drop (candidates)
- `{deleted: 1}` on Todo — no query uses it selectively; verify with
  `$indexStats` before dropping

### Rewrite instead of index
- `User.find({name: {$regex: q, $options: "i"}})` (`…/users.ts:55`) — unanchored
  case-insensitive regex cannot use an index; use a normalized field or Atlas Search

### Already covered
<one line per shape that an existing index serves — keeps the review auditable>

### Not reviewed
<excluded files, dynamic filters that could not be resolved, unknown data sizes>
```

Omit empty sections. For a PR, report only shapes the diff adds or changes,
plus any existing index the diff makes redundant.

## Rules

- Read-only: do not edit schemas, create indexes, or connect to production.
- Every recommendation cites at least one `file:line` that issues the query.
- Give the exact `schema.index(...)` line to add, in the model's existing style.
- When the user wants the indexes added, hand off to `mongoose-schema-safety`
  for the rollout (build before deploy on large collections, `autoIndex`, and
  tests).
