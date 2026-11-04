# Terreno skills

Agent skills for [Terreno](https://github.com/TerrenoLabs/terreno), shipped as one plugin:

| Plugin | What it is |
| --- | --- |
| `terreno` (Claude Code) / `terreno-planning` (Cursor, Codex) | Lifecycle (Grow → Pick ⇄ Roast → Brew → Taste), goal-driven scans (Aim → Sweep → Sift → Plot → Track), PRD, app-building, docs, deployment, and verification skills |

## Install

```bash
# Any agent, via skills.sh
npx skills add TerrenoLabs/terreno-skills

# Claude Code
/plugin marketplace add TerrenoLabs/terreno-skills
/plugin install terreno@terreno-plugins

# Codex
codex plugin marketplace add TerrenoLabs/terreno-skills
```

See [plugins/README.md](plugins/README.md) for each stage's contract.

## Layout

- `plugins/terreno-planning`: Cursor/Codex plugin tree
- `plugins/terreno-claude`: Claude Code plugin tree (scan skills are named `scan-*`)
- `skills/`: flat installable copy for `npx skills add`
- `.claude-plugin/`, `.cursor-plugin/`, `.agents/plugins/`: marketplace manifests
