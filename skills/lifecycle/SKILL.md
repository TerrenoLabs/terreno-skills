---
name: lifecycle
description: "Terreno delivery lifecycle in one skill: PRD, Grow (plan), Pick (build), Roast (prove), Brew (open the PR), Taste (react to CI and review), and the outer loops that drive them. Use when asked to plan, shape, spec, or scope work, implement an approved plan, verify a task, open or update a PR, fix failing CI or answer review bots, or run the planning loop."
---

<!-- GENERATED from bundles.json by .github/scripts/bundles.py. Do not edit here. -->

# Terreno lifecycle bundle

PRD seed, then bounded Grow → Pick ⇄ Roast → Brew → Taste, plus the Pick-Roast, planning, and taste-sweep outer loops.

This skill bundles 9 Terreno skills into one install. Each member is a
complete guide under `references/<skill>/GUIDE.md`, with its own references, scripts, and
agents beside it.

## How to use this bundle

1. Match the request to one row in the table below.
2. Read that guide in full before acting. Resolve the guide's relative links
   (`references/...`, `scripts/...`, `agents/...`) from the guide's own folder.
3. When a guide tells you to invoke or load another skill by name:
   - installed as its own skill: invoke it as usual;
   - listed in the table below: read its guide here and follow it instead;
   - neither: say which skill is missing and offer
     `npx skills add TerrenoLabs/terreno-skills --skill <name>`.

## Guides

| Skill | Guide | Read when |
| --- | --- | --- |
| `terreno-prd` | [references/terreno-prd/GUIDE.md](references/terreno-prd/GUIDE.md) | Interview the app owner and write a full product requirements document (problem, why now, solution, user stories, measurable success metrics, constraints, rollout, out of scope), then publish it where the repository tracks work. Sized for one owner and one or two developers. Runs ahead of Grow; explicit invocation only. |
| `terreno-1-grow` | [references/terreno-1-grow/GUIDE.md](references/terreno-1-grow/GUIDE.md) | Research, clarify, shape, and approve an implementation-ready IP and task list. Use whenever the user asks to plan, shape, spec, or scope substantial work ("help me plan X", "how should we build Y") or to revise an existing plan; not for implementation or PR operations. |
| `terreno-2-pick` | [references/terreno-2-pick/GUIDE.md](references/terreno-2-pick/GUIDE.md) | Implement one approved IP/task slice with behavior-focused TDD, then roast it and pick the next unblocked task until the approved list is done. Not for planning, skipping Roast, or PR submission. |
| `terreno-3-roast` | [references/terreno-3-roast/GUIDE.md](references/terreno-3-roast/GUIDE.md) | Independently prove or disprove the current task against its IP criteria, then return. Do not pick or start the next task. Pick owns the inner loop. Use after Pick, preferably in a fresh context; not for fixing implementation code. |
| `terreno-4-brew` | [references/terreno-4-brew/GUIDE.md](references/terreno-4-brew/GUIDE.md) | Move a Roast-verified implementation into GitHub review: final checks, branch hygiene, commit/push, PR setup, evidence attachment, confirm product CI on every discovered host (GitHub Actions, CircleCI, Buildkite, and similar), and wait in-process for async review bots (Bugbot, CodeQL) before exit. |
| `terreno-5-taste` | [references/terreno-5-taste/GUIDE.md](references/terreno-5-taste/GUIDE.md) | Perform one reactive iteration against the PR's current head. Wait through provider CLI hooks until async review bots and product CI finish (GitHub CLI or CircleCI CLI in a watch loop), inspect every discovered host, mergeability, and reviews, act on what is actionable. Record failed tests from the last CI run. Before any push: fetch latest master (merge only when needed), re-verify those last-run failed tests locally, then run the repository's prepush script when present (otherwise lint and typecheck affected packages) in a no-context subagent, then push and watch CI. Emit state and exit. Invoked directly by a human, it repeats bounded reactions itself until PASS, BLOCKED, or FAIL and never hands a wait back to the human. Never leaves a pushed PR red: answers every review-bot comment and escalates to the human after three failed fix rounds. |
| `terreno-pick-roast-loop` | [references/terreno-pick-roast-loop/GUIDE.md](references/terreno-pick-roast-loop/GUIDE.md) | Drive an approved plan through every Pick–Roast cycle until all tasks pass or a genuine human decision is required. Continue through recoverable engineering failures, keep a complete run ledger, and when input is required present the overall state, completed work and evidence, options, recommendation, and exact question. Not for Grow, Brew, Taste, or CI monitoring. |
| `terreno-planning-loop` | [references/terreno-planning-loop/GUIDE.md](references/terreno-planning-loop/GUIDE.md) | Drive the planning plugin from the current task list, optionally restricting which stages run (Grow, Pick, Roast, Brew, Taste). Not a sixth stage — an outer loop that invokes existing stage skills. Use when asked to run the planning loop, walk the task list, or restrict work to selected phases. |
| `terreno-taste-sweep` | [references/terreno-taste-sweep/GUIDE.md](references/terreno-taste-sweep/GUIDE.md) | Outer loop over open PRs you authored that currently have a merge conflict, a failing product-CI job on any discovered host (GitHub Actions, CircleCI, Buildkite, and similar), or an unanswered review-bot thread. Isolates each PR and reinvokes Taste until mergeable or blocked. Skip drafts and already-green PRs. |

## Installing a different slice

Every member also installs alone
(`npx skills add TerrenoLabs/terreno-skills --skill terreno-prd`), and `npx skills add TerrenoLabs/terreno-skills` opens a
picker grouped by the same bundles.
