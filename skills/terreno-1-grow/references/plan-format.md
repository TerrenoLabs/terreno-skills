# Plan format — what an IP holds

Every IP Grow writes has the same shape, top to bottom:

1. The brief
2. `## E2E tests`, `## Regression cases`, `## User guide`, `## Design`
3. `## Assumptions`
4. The task list
5. `## Open questions (recommendation assumed)`, `## Expansions (follow up later)`,
   `## Decisions`, `## Sign-off`

A fresh Pick agent reads only this file. Anything it needs that is not here, it will guess.

## The brief (top of the IP)

The IP opens with a standalone brief, because a reviewer's link lands here:

```markdown
# <Change title>

<Orientation: three to five sentences on where the repository is, where this takes it,
why now, and who feels the difference. No paths, no task IDs.>

## The idea

<The contract, model, API, or seam that changes, and what is observably different.
One line on the rejected alternative when a reviewer would ask.>

## The plan

| # | Task | Depends on | Lands in | Proves it |
| --- | --- | --- | --- | --- |

Tracer: <seam the first task cuts through>
E2E: <planned specs and layers, e.g. "2 specs (browser, http)"; or "None — reason">
Regression: <provisional case IDs and destination suite; or "None — reason">
User guide: <guide pages added, updated, or retired; or "None — reason">
Design: <canvas link and the artboards the plan builds; or "None — reason">
Out of scope: <tags; see Expansions>
Open risks: <none, or one line each>
```

The `E2E:`, `Regression:`, `User guide:`, and `Design:` lines summarize the sections below.
They stay lines under the plan table, not headings.

## Testing, user guide, and design sections (after the brief)

`## E2E tests` and `## Regression cases` follow the
[`testing plan`](testing-plan.md), then `## User guide` follows the
[`user guide`](user-guide.md) contract, then `## Design` follows
[`designing`](designing.md#the--design-section). Each may be `None — <reason>`. None may be
missing, and a bare `None` with no reason is a defect the cut blocks on.

```markdown
## E2E tests

| ID | Spec or flow | Layer | Proves | Written in |
| --- | --- | --- | --- | --- |
| E1 | <path the e2e guide prescribes> | <a layer from the guide> | <criterion, in observable terms> | T2 |

## Regression cases

Destination: <AREA> → <regression suites>/<area>.md

| ID | Case | Steps | Expected | Platforms | Automated by | Added |
| --- | --- | --- | --- | --- | --- | --- |
| <AREA>-new-1 | <case> | <starting state, then action> | <what is observable> | <platforms> | E1, or manual | <IP slug> |

## User guide

| ID | Page | Change | Audience | Written in |
| --- | --- | --- | --- | --- |
| G1 | <user guide>/<area>/<feature>.md | new, update, or retire | user, admin, or staff | T2 |
```

Rules:

- Every UI or cross-process acceptance criterion has an `## E2E tests` row, written in
  the task that delivers its behaviour, or the section says why it has none. Automate
  first: anything an e2e guide layer can drive and assert is an e2e row.
- `## Regression cases` is usually `None — no hard-to-automate change`. A case is only
  for what a developer or QA must check by hand (push notifications and other hardware
  or OS behavior, a full cross-device flow, feel) that no existing case covers. A
  repository that opts out writes `None — regression suites opted out`.
- Every acceptance criterion that changes what a user sees or does has a `## User guide`
  row, written in the task that delivers its behaviour, or the section says why it has
  none (`None — no user-visible change`). A repository whose `## User guide conventions`
  table says `none` writes `None — user guide off`.
- Regression IDs stay provisional (`<AREA>-new-<n>`), with one `Destination:` line per
  prefix. Brew assigns the real IDs. A row that edits an existing case keeps its real ID.
- When no file exists at the resolved e2e guide path, a task writes it there, and every
  task that writes a planned spec depends on that task.

## Assumptions

One line per implementation detail chosen from repository convention, with the evidence:
`- Cursor pagination reuses the existing paginate helper (api/src/paginate.ts).` Write
`None.` when there are none.

## The task list

Write each task as one checkbox line, then its details in an indented block:

```markdown
- [ ] **T1** — Add the cursor field to the reports API
  - Depends on: none
  - Files: backend/src/api/reports.ts, backend/src/api/reports.test.ts
  - Criteria:
    - `GET /reports?cursor=<id>` returns the reports after that id
  - Seam: ...
  - Interface: ...
  - Cases: ...
  - Blast radius: ...
  - Test skills: ...
  - Verify: `bun test backend/src/api/reports.test.ts`
  - Docs: docs/reference/reports-api.md
  - Skills: terreno-backend-api
  - Design: <artboards and states, UI tasks only>
```

- The title is the commit subject for the task, so it reads as one behaviour.
- `Depends on:` is `none` or task IDs separated by commas and/or `and`. A missing line
  means the previous task in IP order; the first task defaults to none.
- `Files:` names every file the task writes, including shared registries, barrels, and
  route or tool indexes.
- `Docs:` names the architecture, reference, or how-to pages the task updates, per the
  documentation contract. Docs are never a later task.
- Unknown IDs, self-dependencies, and cycles are defects.

## The test brief

Every task carries a test brief in its details block. Pick writes the task's tests from the
brief, the task's criteria, and the IP's brief and Decisions, before anyone implements it,
in a context that never sees the implementation. So the brief is all the test writer knows.
Write it so a tester who has never seen this conversation could write thorough tests:

```markdown
- [ ] **T2** — Page the reports list with a cursor
  - Depends on: T1
  - Files: backend/src/api/reports.ts, backend/src/api/reports.test.ts
  - Seam: GET /reports (HTTP route)
  - Interface: `GET /reports?limit=<n>&cursor=<id>` → `{data: Report[], next: string | null}`,
    exactly those fields (each Report: `_id`, `title`, `created`); staff only
  - Cases:
    - 3 reports, limit 2 → data r1, r2; next = r2's id
    - cursor = r2's id → data r3; next null
    - cursor of a deleted report → 400 `{title: "Invalid cursor"}`
    - limit 0 or 101 → 400
    - patient user → 405 (list permission); no token → 401
  - Blast radius: report deletion reads the same index → backend case in reports.test.ts
  - Test skills: terreno-backend-tests
```

- **Seam**: the highest public seam that proves the behavior (HTTP route, exported
  function, rendered component, adapter contract).
- **Interface**: what a caller writes and gets back, precise enough to code a test against
  before it exists: signature or route, inputs, output shape, errors, who may call it.
- **Cases**: worked examples with literal inputs and expected values. Include the edge
  cases that matter: empty, missing, and invalid input; boundaries; permissions with exact
  statuses; loading and error states for UI. A writer with only "handles errors" has
  nothing to assert.
- **Blast radius**: for a task that changes state, the consumers that read it and the layer
  each case belongs to (see [Blast radius](#blast-radius)). `none` when the task changes no
  state another behavior reads.
- **Test skills**: the repository skills that say how to write tests at this seam. In
  Terreno apps, `terreno-backend-tests`, `terreno-frontend-tests`, or
  `terreno-mobile-tests`. Their tables decide the layer and the exact permission statuses
  (401 no token, 405 method permission, 403 object permission, 404 missing id), so Cases
  name statuses from them. A route that returns user or PHI data lists its exact response
  fields in Interface, so the test can pin the shape.

A layer with no test setup yet (no preload, the test runner finds nothing) gets its own
first task, built with `terreno-test-setup` in Terreno apps, which the other tasks depend
on. Writing tests first cannot add setup, so setup must already exist.

A task whose criteria no test can observe (prose, config with no behavior) says
`Cases: none (untestable: <why>)`. Roast checks the claim.

A UI task's `Design:` line names each artboard and the states that task delivers:
`Design: Booking.dc.html (empty, loading)`. Those states, and only those, become its Cases
and e2e rows.

### Blast radius

A task that changes state can break behavior it never touches: every screen, query, or job
that reads that state. Trace it when writing the task:

1. Start from the mutation (what the task writes, deletes, or changes the meaning of).
2. List its callers, and the consumers whose result depends on the changed state.
3. Keep only consumers a real user path reaches.
4. A consumer whose dependency is entirely backend logic gets a backend case in that
   consumer's existing suite. A missing case there is the gap, not e2e work.
5. A user-observable consumer gets an e2e case, planned as an `## E2E tests` row.

## Splitting for a parallel build

Put the tracer first: the smallest end-to-end behaviour that proves the main seam. Then
split the remaining work into small, composable tasks. Each task is one independently
testable behaviour that can be roasted on its own; split any task that needs more than one
roast-able behaviour.

Declare real prerequisites rather than depending on the previous task by habit: depend on
a task only when this one reads or extends something it creates. Two tasks that share a
`Files:` entry depend on each other, so their writes are ordered. Prefer wide over deep:
fan out independent tasks and keep dependency chains short. A chain longer than three
needs a reason for each link. Use a join task only when a behaviour requires the branches
to be complete.

For example, after a tracer adds a reports API, a reports client and an export utility
can both depend on the tracer if they write different files. If both write the same
client file, order them with a dependency. The cut attacks false independence, tasks that
contain multiple behaviours, and chains that could fan out.

## Bottom sections

These close every IP, in this order, after the task list.

```markdown
## Open questions (recommendation assumed)

| ID | Question | Recommendation | Why | If answered differently | Tasks affected |
| --- | --- | --- | --- | --- | --- |
| Q4 | <the question as it was asked> | <the choice the plan is built on> | <one line, cite evidence> | <what changes> | T2, T4 |

## Expansions (follow up later)

| ID | Idea | Why it came up | Rough size | Depends on |
| --- | --- | --- | --- | --- |
| X1 | <scope beyond this request> | <what surfaced it> | S / M / L | <task or decision> |

## Decisions

| ID | Question asked | Answer | What it changes |
| --- | --- | --- | --- |
| Q1 | <the question as it was asked> | <the settled choice> | <the design consequence> |

## Sign-off

Status: draft | approved <date>
Cut: <rounds> rounds, <n> findings: <edited> fixed, <grilled> grilled, <moved> moved to questions or expansions, <rebutted> rebutted
```

Rules:

- Open questions hold only what the human deferred (see
  [`grilling`](grilling.md#deferral)), plus cut findings carried past the second round.
  A fundamental question never appears there.
- "If answered differently" is required. It is what lets someone judge a question without
  reading the plan. Answering one later moves it to Decisions and rewrites the tasks it
  names.
- Question IDs are shared across Decisions and Open questions, in the order asked.
- Expansions are not promises. Pick never builds them.
- Empty sections stay with a single `None.` line so the reader can see nothing was hidden.
- An IP approved before this format reads a missing bottom section as
  `None — predates contract`.

## Anti-patterns

- Building an expansion "because it was small"
- An Open question without a recommendation, or without "If answered differently"
- A test brief with no Interface, Cases without literal expected values, or a
  state-changing task with no Blast radius
- A UI criterion with no planned spec, or a testing section that says only `None`
- A UI task with no `Design:` line when the IP has a design
- Two tasks that write the same file with no dependency between them
- A chain of dependencies that could be a fan-out
