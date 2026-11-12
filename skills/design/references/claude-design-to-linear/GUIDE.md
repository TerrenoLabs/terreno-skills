<!-- GENERATED copy of skills/claude-design-to-linear/SKILL.md. Do not edit here. -->

# Claude Design to Linear

Convert a Claude design into actionable Linear projects and issues. Each project's `IP:`
issue is the input a later Grow run (with `design-blend`) shapes into an approved IP.

## Non-negotiable rules

1. **Verify Linear access first.** Use the Linear MCP server when it is connected;
   otherwise use the GraphQL API with `LINEAR_API_KEY`. If neither works, stop.
2. **Inventory existing projects before creating anything.** Fetch all existing Linear
   projects and their issues. Update matching projects; never duplicate.
3. **Confirm the plan before mutating Linear.** Show the full list of projects to create
   or update and wait for explicit confirmation.
4. **One project per distinct screen or interaction surface.** Prefer more small projects
   (2–5 days each, hard cap 1 week) over fewer large ones.
5. **Each project gets exactly two issues:** `IP: $feature` and `Execute: $feature`.
6. **Use the design as evidence.** Reference exact screen labels and visual details from
   the design in issue descriptions.

## Workflow

### Step 0: Verify Linear access

- **MCP:** list the Linear server's tools and inspect the schemas you need. If the server
  needs authentication, stop and tell the user to authenticate it, then retry. Do not
  guess tool names or parameters.
- **API key:** check for `LINEAR_API_KEY`. If absent, stop:

  > "Linear access not found. Connect the Linear MCP server or set LINEAR_API_KEY, then
  > re-run."

  Verify with `{ viewer { id name } }` and abort on 401.

If the target team or workspace is ambiguous, inspect existing projects first. Ask the user
only when the data cannot disambiguate.

### Step 1: Load and understand the design

1. If the design is a handoff bundle, read its `README.md` to identify the primary design
   file.
2. Read the primary design file **in full**. Do not skim.
3. Extract every screen label (`data-screen-label` attributes, frame names, or section
   comments).
4. Note visual patterns shared across screens (shell, header, nav bar). These become a
   **Shell** project.
5. List every distinct interaction surface (screen, modal, FAB action, and so on).

### Step 2: Inventory existing Linear projects

Fetch all projects, following `pageInfo.hasNextPage` until every page is loaded. With the
API key:

```graphql
query Projects($after: String) {
  projects(first: 100, after: $after) {
    pageInfo { hasNextPage endCursor }
    nodes {
      id
      name
      description
      status { name }
      issues(first: 100) {
        pageInfo { hasNextPage endCursor }
        nodes { id title }
      }
    }
  }
}
```

If a matched project's `issues.pageInfo.hasNextPage` is true, page that project's issues
before deciding whether `IP:` or `Execute:` issues already exist. With MCP, use the
equivalent list and get tools and page the same way.

Match on exact or normalized titles, the same feature slug, the same design link, or the
same scoped deliverable under a weaker title. Categorize each project as **match**
(update), **related** (note but don't touch), or **new** (create). When in doubt between
updating and duplicating, update.

### Step 3: Slice into projects

- **Shell and navigation first.** If screens share a layout shell, nav bar, or header,
  that is project #1.
- **One screen = one project.** Each distinct tab or full-screen view is its own project.
- **Modals and FAB flows.** An overlay tightly coupled to one screen belongs to that
  screen's project. One that appears on several screens gets its own project.
- **Scope cap.** If a screen's backend plus frontend is more than a week of work, split
  further (for example, list view separate from detail view).
- **Lean toward more projects.** When in doubt, split.

### Step 4: Build the plan

For each project, draft:

- Project name (`Feature Area — Screen Name`)
- Description (≤ 255 characters)
- Design evidence: exact screen label(s) from the design
- Scope, and out of scope (pushed to a later iteration)
- Dependencies (other projects, or models and APIs required first)
- Acceptance criteria (testable bullets)
- Regression test steps (a manual walkthrough a QA engineer could follow)
- Issue titles: `IP: $feature` and `Execute: $feature`

Print the full plan as a concise table and ask for confirmation:

> "Ready to create/update N projects and 2N issues in Linear. Reply `yes` to proceed."

Do not mutate Linear until you receive explicit confirmation.

### Step 5: Execute in Linear

For each project, in dependency order:

1. **Updating:** refresh the project's name and description.
2. **Creating:** create the project with the team's Planned (or equivalent) status.
3. Find existing planning issues for the feature, including current `IP: $feature` titles
   and legacy `Implementation Plan: $feature` titles.
4. Update or retitle the existing planning issue to `IP: $feature`. Create it only if no
   matching planning issue exists.
5. Update the existing `Execute: $feature` issue. Create it only if none exists.
6. If duplicates already exist, do not create more. Report them and ask which to keep.
7. If an initiative was specified, link each project to it.

Do not close or replace existing projects or issues unless they are clearly superseded,
and name every one you did in the report.

### Step 6: Report

Print a summary table:

| Action | Project | Issues |
|---|---|---|
| Updated | Messaging — Thread | IP + Execute |
| Created | Messaging — Inbox | IP + Execute |

List any splits made to keep scope small, and any existing work that was reused or
retitled.

---

## Project description format (≤ 255 characters)

One sentence covering what surface, what data, and what the user can do. No fluff.

---

## Issue templates

### `IP: $feature`

```markdown
## Design evidence
<!-- Screen label(s) from the design file, e.g. "Opt 2 — Home" -->
- Screen: <label>
- Key visual details: <2-3 specific UI details that anchor the design intent>

## Scope
-

## Out of scope
-

## Dependencies
<!-- Other projects, models, or APIs that must exist first -->
-

## Acceptance criteria
<!-- High-level, testable outcomes. Detailed criteria live in the Execute issue. -->
-

## Regression test steps
1.
2.
3.

## Open questions
-
```

### `Execute: $feature`

```markdown
## Design evidence
- Screen: <label>
- Key visual details: <specific measurements, colors, interaction states from the design>

## Scope
-

## Out of scope
-

## Dependencies
-

## Acceptance criteria

### Backend
-

### Frontend
-

### Edge cases / error states
-

## Regression test steps
1.
2.
3.
```

---

## Success checklist

- [ ] Linear access confirmed before any mutation.
- [ ] All existing projects inspected; no duplicate projects created.
- [ ] User confirmed the project plan before Linear was mutated.
- [ ] Every project has exactly one `IP:` issue and one `Execute:` issue.
- [ ] Every issue includes design evidence (screen label plus visual details).
- [ ] Every project and issue includes acceptance criteria.
- [ ] Every project and issue includes regression test steps.
- [ ] No project exceeds about one week of work.
- [ ] Projects linked to the specified initiative, if one was given.

## Forbidden actions

- Do not create issues without design evidence.
- Do not create projects larger than a week; split instead.
- Do not create separate `Backend` / `Frontend` execution issues; use one `Execute:` issue
  per project with Backend and Frontend acceptance sections.
- Do not duplicate existing projects; update them.
- Do not mutate Linear without user confirmation of the plan.
- Do not paste the full design into issues.
