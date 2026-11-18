---
name: terreno-1-grow
description: Research, triage, grill, shape, attack, and approve an implementation-ready IP and task list. Grills every fundamental decision to the bottom, lets the human defer the rest onto an Open questions table with the recommendation assumed, writes a test brief per task, plans e2e, regression, user guide, and design work, attacks the draft with a fresh requester-side cut subagent, and asks for approval last. Use whenever the user asks to plan, shape, spec, or scope substantial work ("help me plan X", "how should we build Y") or to revise an existing plan; not for implementation or PR operations.
---

# Grow — shape

Turn a request, ticket, or specification into an approved IP a fresh Pick agent can
execute without conversation history.

Read before acting:

- [`grilling`](references/grilling.md): triage, rounds, deferral, approval last, and the
  approval brief
- [`plan format`](references/plan-format.md): the IP brief, testing, user guide and design
  sections, task format, test brief, splitting, and the bottom sections
- [`cutting`](references/cutting.md): the requester-side attack on the draft
- [`designing`](references/designing.md): Claude Design canvases, design work, design
  questions, the `## Design` section, and the snapshot
- [`testing plan`](references/testing-plan.md): the e2e guide and the two required
  testing sections
- [`user guide`](references/user-guide.md): the end-user guide and the required
  `## User guide` section
- [`lifecycle contract`](references/lifecycle-contract.md),
  [`documentation contract`](references/documentation-contract.md), and
  [`PR deployments`](references/pr-deployments.md)

## Preconditions

- A request/spec/ticket and repository are available.
- This invocation owns shaping only. After `PASS`, Pick and Roast run the inner loop.

## Inputs

- Request/spec/ticket and linked context, verbatim
- A Claude Design link, or a canvas named in an existing `## Design` section, with its
  snapshot
- Existing IP/task files, if revising
- Repository instructions, architecture docs, code, tests, history, and project skills
- Execution state and prior result, when present

## Procedure

1. **Reconstruct.** Use the repository's IP convention. Otherwise use
   `docs/plans/YYYY-MM-DD-<slug>.md` with the task list in the same file, and execution
   state at `.terreno/pipeline/<slug>.json`. Avoid a shared mutable index. Read prior
   state and verify it against repository reality. An IP approved before the testing-plan,
   user-guide, or design contracts reads a missing section as `None — predates contract`;
   revising it adds the section.
2. **Read architecture docs** for the affected area. Treat them as the current design. If
   docs are missing or contradict the code, the IP resolves that in this invocation.
   Resolve the e2e guide, regression suites, and smoke command from the agent
   instructions' `## Testing conventions` table or the defaults (`docs/testing/e2e.md`,
   `docs/regression/`), and read the guide and the area's suites. Resolve the user guide
   path from the `## User guide conventions` table or the default (`docs/user-guide/`) and
   read the area's pages, unless the value is `none`. Read the design the request or an
   existing `## Design` section names, per [`designing`](references/designing.md#reaching-the-canvas).
3. **Discover supporting skills.** Inspect available repository/project skills and load
   those relevant to the affected domains, including documentation and testing skills.
   Record selected skills for downstream stages.
4. **Research before asking.** Answer every discoverable fact yourself, with explore
   subagents in parallel. Never ask the human something the repo, docs, or git history can
   answer.
5. **Triage** every open question per [`grilling`](references/grilling.md#triage-every-open-question):
   fact, implementation detail, deferrable decision, fundamental decision, or expansion.
   Decide whether the request is [design work](references/designing.md#design-work): it
   asks how something should look or flow, or changes the design. Design work is part of
   this run: start a canvas when there is none, launch the app and screenshot the screens
   it touches, and draw the proposed versions, with options where the shape is open.
6. **Grill.** Follow [`grilling`](references/grilling.md) for every human decision. Work
   the frontier in rounds of selectable options with a recommended default, using the
   harness's structured question tool when it has one. Fundamental decisions are grilled
   to the bottom and block writing. Every deferrable question also offers
   `Use the recommendation (list as open)`; picking it is consent, and the question goes
   to the Open questions table. A question about a screen is a
   [design question](references/designing.md#design-questions): its options are designs.
   Wait for explicit shared-understanding confirmation before writing. Every
   wait-for-human or done message closes with PR deployment URLs when a PR has them.
7. **Shape.** Contracts, models, and APIs before implementation detail. Scope, non-scope,
   architecture decisions, risks, human gates, rollout, dependencies. Put the tracer
   first, then split the work into the smallest independently testable behaviours per
   [`plan format`](references/plan-format.md#splitting-for-a-parallel-build). Park
   scope beyond the request in Expansions, never in the task list.
8. **Specify proof.** Every acceptance criterion is observable and names its verification
   method (test, build, runtime/API/database probe, UI exercise, artifact). "Manual check"
   is not one. Give every task a [test brief](references/plan-format.md#the-test-brief)
   (Seam, Interface, Cases, Blast radius, Test skills): Pick writes the task's tests from
   it before any implementation, so it must stand alone. Pair each UI or cross-process
   criterion with a planned spec at the path and layer the e2e guide gives, written by the
   task that delivers the behaviour, or state why it has none. Add a regression case only
   for what a person must check by hand, per the [`testing plan`](references/testing-plan.md).
   Pair each criterion that changes what a user sees or does with a `## User guide` row,
   or state why it needs none. Give each UI task a `Design:` line naming the artboards and
   states it builds. When the input is a PRD from `terreno-prd`, carry each success metric and
   guardrail into an acceptance criterion, grill each `TBD` as a human decision, and do
   not re-ask product decisions the PRD already settled.
9. **Write** the IP per [`plan format`](references/plan-format.md): the brief, then
   `## E2E tests`, `## Regression cases`, `## User guide`, and `## Design` (each may be
   `None — <reason>`, none may be missing), then Assumptions, the task list (every task
   with `Depends on:`, `Files:`, criteria, test brief, verification, docs, supporting
   skills), then Open questions, Expansions, Decisions, and Sign-off. When no file exists
   at the resolved e2e guide path, add a task that writes it, and make every task that
   writes a planned spec depend on it. Docs updates follow the documentation contract
   and are not deferred. Set `Status: draft`.
10. **Cut, then fix.** Run [`cutting`](references/cutting.md): a fresh subagent that sees
    only the human's words and the IP attacks the draft and returns findings. For each:
    - edit the IP so it holds;
    - grill it, when it is a human decision (one more round, same rules; a deferral moves
      it to Open questions);
    - move it to Expansions, when it is new scope;
    - rebut it in one line with evidence (a file, a quote from the human), when the
      attack is wrong.

    A `Couldn't assess` line is unchecked, not passed: check it yourself, or record it in
    Assumptions or Open questions. Every blocking finding is edited, grilled, moved, or
    rebutted. When a blocking finding changed the plan, cut once more. Stop after two
    rounds and carry anything left into Open questions. Record the tally in Sign-off.
11. **Approve.** Approval is only ever the last question. With a design, write the
    [snapshot](references/designing.md#the-snapshot) first and record the canvas version
    in `## Design`. Post the standalone [approval brief](references/grilling.md#approval-brief),
    then ask one structured question, `Approve (Recommended)` against `Change something`.
    A change returns to the step it affects; a structural change cuts again. Only after
    explicit approval set `Status: approved <date>`, commit the snapshot with the IP,
    update execution state, and emit the stage result collapsed per the lifecycle
    contract.

Remaining Open questions are fine at approval: the human chose to defer them, and Pick
builds on their recommendations.

## Supporting skills

Follow the shared discovery procedure. Supporting skills may cover API/UI architecture,
data access, schemas, prompts, deployment, testing, or safety. Names are repository-defined;
none is universally required. In Terreno apps the test briefs name
`terreno-backend-tests`, `terreno-frontend-tests`, or `terreno-mobile-tests`.

## Evidence produced

- Approved IP path (task list inside it unless the repository splits them)
- Standalone approval brief
- Research findings and recorded assumptions (not chain-of-thought)
- Decisions, each with the question that prompted it; Open questions with the
  recommendation assumed; Expansions
- Acceptance-criterion → verification mapping and a test brief per task
- `## E2E tests`, `## Regression cases`, `## User guide`, and `## Design` sections
- Cut tally: rounds, findings, and how each was resolved
- Selected supporting skills and docs files named on each task
- Updated execution state and structured Grow result

## Success conditions

- The IP is approved, implementation-ready, dependency-aware, and testable.
- A fresh Pick invocation can find the next unblocked task, its criteria, test brief,
  decisions, assumptions, and supporting skills in the IP alone.
- A reviewer with no prior context can approve or push back from the brief alone.
- Every question the human deferred is visible in Open questions with the recommendation
  the plan assumed.
- Emit `PASS` with `next: pick`.

## Failure conditions

Malformed or contradictory artifacts emit `FAIL` with exact defects, `next: grow`, and a
focused Grow retry. Do not pass incomplete criteria or test briefs to Pick.

## Blocked conditions

An unresolved fundamental decision, missing approval, unavailable required
evidence/access, or unsafe ambiguity emits `BLOCKED` with `next: null`, options,
tradeoffs, and a recommended default when appropriate.

## Recommended next stage

- `PASS` → Pick
- `FAIL` → Grow with defect evidence
- `BLOCKED` → outer loop routes the named human/external gate
