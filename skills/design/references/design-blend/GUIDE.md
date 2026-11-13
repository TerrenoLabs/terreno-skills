<!-- GENERATED copy of skills/design-blend/SKILL.md. Do not edit here. -->

> Bundled copy of the `design-blend` skill. Its skill directory (`<skill-dir>`, "this
> skill's folder") is the folder holding this guide, `references/design-blend/` inside
> the bundle, so `scripts/`, `references/`, `examples/`, and `agents/` paths resolve from here.

# Design Blend

Use this skill when the work starts from a Claude design (a design file, an HTML handoff
bundle, or screenshots of one) and the target is a Terreno app. It is a supporting skill
for **Grow**: it supplies the design-specific sections of the IP and task list. Approval,
implementation, and verification stay with the lifecycle stages.

## Non-negotiable contract

1. **REST-first backend design.**
   - Every persistent entity maps to a model and a `modelRouter` CRUD plan first.
   - Custom actions are forbidden unless they pass the Action Decision Gate.
2. **Auditable action gating.**
   - Track both approved and rejected action candidates.
   - If rejected candidates are missing, the output is invalid.
3. **Terreno-first UI composition.**
   - Map each design section to existing `@terreno/ui` components before proposing new
     components.
4. **New components are conditional, never default.**
   - A new component is allowed only if a concrete composition gap is proven.
5. **Human approval before implementation.**
   - The IP and task list go through Grow's approval brief. Nothing is implemented until
     the human approves.
6. **Lifecycle-driven implementation.**
   - After approval, Pick implements each task and Roast proves it. Do not run a separate
     implementation loop from this skill.
7. **Per-task Plan vs Actual.**
   - Every Roast result for a design task carries a Plan vs Actual record with status
     `match`, `partial`, or `deviation`.

If any item above is skipped, stop and correct it before proceeding.

## Documentation

Read the app's architecture docs and `docs/reference/` for the affected area before
mapping the design. Every user-visible or architectural slice names docs to create or
update. Write those pages with `update-docs` in the same slice.

## Reading the design

1. If the design is a handoff bundle, read its `README.md` to find the primary design file.
2. Read the primary design file in full. Do not skim.
3. Extract every screen label (`data-screen-label` attributes, frame names, or section
   comments) and every distinct interaction surface: screen, modal, sheet, FAB action.
4. Note shared chrome (shell, header, tab bar). It becomes its own task or slice.
5. Record assumptions where the design is silent (empty states, errors, permissions).
   Product, data-ownership, and permission gaps are human decisions for Grow's grilling.

## Required IP sections

Write these into the IP, in this order.

### 1) Model Inventory

For each inferred entity:

- `modelName`
- `fields` (`name`, `type`, `required`, `default`, `description`)
- `relations` (`ref`, cardinality)
- `indexes`
- `plugins`
- ownership and multitenancy notes (`ownerId`, tenant key, soft delete)

Artifacts:

1. **Model Inventory** table.
2. **Per-model schema checklist.** Schema changes follow `mongoose-schema-safety`.
3. **No model needed** rationale for presentational-only sections.

### 2) REST Endpoint Matrix

For each model, define a `modelRouter` plan:

- base path
- CRUD endpoints:
  - `POST /resource`
  - `GET /resource`
  - `GET /resource/:id`
  - `PATCH /resource/:id`
  - `DELETE /resource/:id` (or an explicit disable reason)
- `permissions` by method
- `queryFields`
- `queryFilter` (ownership or tenant filter when relevant)
- `sort`
- `populatePaths` when needed

Artifacts:

1. **REST Endpoint Matrix** table (`method`, `path`, `permission`, `purpose`).
2. **modelRouter options block** for each model.
3. Explicit CRUD disable rationale when applicable.

### 3) Action Decision Gate

An action candidate is eligible only if at least one is true:

1. non-resource command semantics (`publish`, `approve`, `submit`, `duplicate`)
2. an aggregation or read-model shape CRUD cannot express efficiently
3. a performance path with measurable benefit

For each candidate:

- `actionName`
- `method` + `path`
- `whyRestIsInsufficient` (mandatory)
- `requestSchema` + `responseSchema`
- `permissions`
- `performanceNote` (mandatory for performance-motivated actions)

Artifacts:

1. **Action Decision Gate** checklist.
2. **Approved Actions** table.
3. **Rejected Candidate Actions** table. Mandatory; write "none rejected" when empty.

### 4) Terreno Component Mapping

For every screen and state:

- map sections to existing `@terreno/ui` components first (`Page`, `Box`, `Card`,
  `DataTable`, `TextField`, `SelectField`, `Button`, `Modal`, `Spinner`, `Toast`, and so on)
- include loading, empty, error, and success states
- include navigation and interaction flow

Artifacts:

1. **Terreno Component Mapping** table by screen section.
2. **State Coverage Matrix** (`loading`, `empty`, `error`, `success`).
3. **Accessibility and testability notes** (`testID`, semantics).

### 5) New Component Contract (conditional)

A new component is forbidden unless a proven gap exists.

Proof:

1. attempted composition with existing `@terreno/ui` components
2. explicit mismatch or gap explanation
3. why wrappers, props, or slotting are insufficient

If approved, require:

- `componentName`
- `whyExistingTerrenoComponentsDoNotFit`
- `propsApi`
- `states`
- `reusabilityTargets` (at least one additional use case)

Artifacts:

1. **New Component Candidates** table.
2. **Approved New Components** API contract section.
3. **Rejected Candidate Components** section with the fallback composition.

## Task list

Write Grow's dependency-aware task list from the sections above:

- models and `modelRouter` endpoints before the screens that consume them
- shared chrome before the screens inside it
- approved actions and approved new components as their own tasks
- each task names the screen labels it implements, its files and seams, acceptance
  criteria tied to the State Coverage Matrix, verification, and docs to update
- each task lists `design-blend` as a supporting skill, and its verification includes the
  Plan vs Actual record below, so Roast produces it without this conversation

Then post Grow's approval brief. Do not implement until the human approves.

## After approval

Pick ⇄ Roast runs the tasks in dependency order. For each design task, Roast's result
includes:

```markdown
### Plan vs Actual: Task <id>
- Status: match | partial | deviation
- Planned:
  - <planned outcomes>
- Actual:
  - <implemented outcomes>
- Evidence:
  - <tests, commands, screenshots>
- Corrective action:
  - <required follow-up, or "none">
```

On `partial` or `deviation`, update the remaining tasks before Pick continues. A deviation
that changes a human decision goes back to the human.

## Quality checks before handoff to Brew

- [ ] Model Inventory and schema checklists are present.
- [ ] REST Endpoint Matrix and `modelRouter` options are present for every model.
- [ ] Action Decision Gate records approved and rejected candidates.
- [ ] Terreno Component Mapping and State Coverage Matrix are present.
- [ ] Any new component has proven-gap evidence and an API contract.
- [ ] The human approved the IP and task list before implementation.
- [ ] Every implemented task has a Plan vs Actual record.
- [ ] Frontend work: `verify-ui-changes` completed (app launched, logged in when required,
      feature exercised) and screenshots or video attached to the PR with
      `attach-pr-media`.

If any box is unchecked, the output is invalid and must be corrected.
