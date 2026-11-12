---
name: design
description: "Terreno design handoff in one skill: blend a Claude design file or handoff bundle into an implementation-ready Terreno plan (REST-first models, @terreno/ui mapping), and break a design into small Linear projects. Use when the input is a design file or handoff bundle to build with Terreno or to turn into Linear issues."
---

<!-- GENERATED from bundles.json by .github/scripts/bundles.py. Do not edit here. -->

# Terreno design handoff bundle

Turn a Claude design into a Terreno implementation plan and Linear work.

This skill bundles 2 Terreno skills into one install. Each member is a
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
| `design-blend` | [references/design-blend/GUIDE.md](references/design-blend/GUIDE.md) | Turn a Claude design file or handoff bundle into an implementation-ready Terreno IP: REST-first models and modelRouter endpoints, a gated list of custom actions, and a @terreno/ui component mapping, then hand off to the Pick/Roast inner loop. Use when the input to Grow is a design; not for designs with no Terreno backend or UI. |
| `claude-design-to-linear` | [references/claude-design-to-linear/GUIDE.md](references/claude-design-to-linear/GUIDE.md) | Turn a Claude design file or handoff bundle into small Linear projects, each with one IP issue and one Execute issue carrying design evidence, acceptance criteria, and regression test steps. Updates existing projects instead of creating duplicates. Use when asked to break a design into Linear work; not for writing the IP itself (Grow, with design-blend) or for implementation. |

## Installing a different slice

Every member also installs alone
(`npx skills add TerrenoLabs/terreno-skills --skill design-blend`), and `npx skills add TerrenoLabs/terreno-skills` opens a
picker grouped by the same bundles.
