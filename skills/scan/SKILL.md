---
name: scan
description: "Terreno goal-driven code scans in one skill: Aim (charter a measurable goal), Sweep (detect), Sift (verify and rank), Plot (slice into PRs), Track (re-measure), plus the campaign and resident loops. Use when asked to scan a codebase for an outcome (build time, N+1 queries, accessibility, maintenance cost), set a long-term engineering goal, or keep scanning and fixing until a metric hits target."
---

<!-- GENERATED from bundles.json by .github/scripts/bundles.py. Do not edit here. -->

# Terreno code scans bundle

Charter a measurable long-term goal, map-reduce the repository into findings (Aim → Sweep → Sift → Plot → Track), and drive each slice to a PR.

This skill bundles 7 Terreno skills into one install. Each member is a
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
| `terreno-scan-1-aim` | [references/terreno-scan-1-aim/GUIDE.md](references/terreno-scan-1-aim/GUIDE.md) | Turn a long-term codebase goal into an approved scan charter — measurable metric, captured baseline, dry-run detection rules, exclusions, validity rule, severity rubric, and slice policy. Use when asked to scan a codebase for an outcome ("improve build time", "find N+1 queries", "reduce maintenance overhead", "make us WCAG-compliant"), to set a long-term engineering goal, or to start or reshape a scan campaign; not for implementation, PR operations, or one-off searches. |
| `terreno-scan-2-sweep` | [references/terreno-scan-2-sweep/GUIDE.md](references/terreno-scan-2-sweep/GUIDE.md) | Run an approved scan charter across the repository — execute detection rules, shard the hits deterministically, and map fresh parallel workers over the shards into schema-valid candidate findings. Use after a scan charter is approved, or to re-sweep a later campaign round; not for shaping goals, ranking findings, or writing code. |
| `terreno-scan-3-sift` | [references/terreno-scan-3-sift/GUIDE.md](references/terreno-scan-3-sift/GUIDE.md) | Reduce raw scan candidates into a trustworthy findings report — dedupe, adversarially verify, drop what does not reproduce or does not move the goal metric, rank by impact over effort, and write the round's findings report. Use after a sweep returns candidates; not for running detection rules, shaping goals, or writing code. |
| `terreno-scan-4-plot` | [references/terreno-scan-4-plot/GUIDE.md](references/terreno-scan-4-plot/GUIDE.md) | Turn ranked scan findings into PR-sized slices and hand the top slice to the Terreno IP and task system, writing a Grow-ready brief with metric-linked acceptance criteria and verification methods for each slice. Use after a sift produces a findings report; not for discovering findings, implementing them, or PR operations. |
| `terreno-scan-5-track` | [references/terreno-scan-5-track/GUIDE.md](references/terreno-scan-5-track/GUIDE.md) | Re-measure a scan campaign's goal metric after slices land, close or reopen findings with evidence, record the round, and choose the next move — more slices, a fresh sweep, or a report with one question. Use after a plotted slice finishes in the lifecycle or a round is dry; not for discovering findings, planning slices, or writing code. |
| `terreno-loop-campaign` | [references/terreno-loop-campaign/GUIDE.md](references/terreno-loop-campaign/GUIDE.md) | Drive a long-term codebase goal to its target — charter it, sweep and sift the repository into findings, plot PR-sized slices, run each slice through the Terreno lifecycle, then re-measure and repeat until the metric hits target or a genuine human decision is required. Not a scan stage — an outer loop that invokes the scan stages and the lifecycle. Use when asked to run a scan campaign, work toward a long-term engineering goal, or keep scanning and fixing until an outcome is reached. |
| `terreno-loop-resident` | [references/terreno-loop-resident/GUIDE.md](references/terreno-loop-resident/GUIDE.md) | Run a scan campaign as a resident session — keep working toward the goal, open PR-sized slices routed to named reviewers, and heartbeat over every open PR to answer review comments, fix failing CI, and land merges, until the metric hits target or a human decision is required. Use when asked to keep a goal running continuously, leave a scan going in the background, watch and respond to campaign PRs, or run the scan loop; not for a single bounded round. |

## Installing a different slice

Every member also installs alone
(`npx skills add TerrenoLabs/terreno-skills --skill terreno-scan-1-aim`), and `npx skills add TerrenoLabs/terreno-skills` opens a
picker grouped by the same bundles.
