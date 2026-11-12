# Installable Terreno skills

Install from GitHub with the skills CLI:

```bash
npx skills add TerrenoLabs/terreno-skills
npx skills add TerrenoLabs/terreno-skills --skill lifecycle
npx skills add TerrenoLabs/terreno-skills --skill terreno-1-grow
```

`app`, `design`, `lifecycle`, `scan`, and `ship` are bundles: each is one skill whose
`references/` holds a copy of its member skills. They are generated from
[`../bundles.json`](../bundles.json) by `python3 .github/scripts/bundles.py`; edit the
member skill, never the copy.

This directory is generated. Canonical sources:

| Source | Owns |
| --- | --- |
| `plugins/terreno-planning/skills/` | Lifecycle, Terreno app, docs, upgrade, deploy, and UI-verification workflows |
| `plugins/terreno-planning/agents/` | Pre-commit and UI verification agents |
| `.rulesync/skills/` | Terreno-repository-only and optional non-conflicting Expo skills |
| `<package>/.ai/skills/` | Package/MCP-specific copies; not installable overlays |

Regenerate with `bun run skills:sync`. Human-facing docs stay the architecture source;
follow `update-docs` and the lifecycle documentation contract.
