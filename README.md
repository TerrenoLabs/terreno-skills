# Terreno skills

Agent skills and plugins for [Terreno](https://github.com/TerrenoLabs/terreno), in two plugin sets:

| Plugin | What it is |
| --- | --- |
| `terreno` (Claude Code) / `terreno-planning` (Cursor, Codex) | Lifecycle (Grow → Pick ⇄ Roast → Brew → Taste), PRD, app-building, docs, deployment, and verification skills |
| `terreno-scan` | Goal-driven code scans: Aim → Sweep → Sift → Plot → Track |

## Install

```bash
# Any agent, via skills.sh
npx skills add TerrenoLabs/terreno-skills

# Claude Code
/plugin marketplace add TerrenoLabs/terreno-skills
/plugin install terreno@terreno-plugins
/plugin install terreno-scan@terreno-plugins

# Codex
codex plugin marketplace add TerrenoLabs/terreno-skills
```

See [plugins/README.md](plugins/README.md) for each stage's contract.

## Layout

- `plugins/terreno-planning`, `plugins/terreno-scan`: Cursor/Codex plugin trees
- `plugins/terreno-claude`, `plugins/terreno-scan-claude`: Claude Code plugin trees
- `skills/`: flat installable copy for `npx skills add`
- `.claude-plugin/`, `.cursor-plugin/`, `.agents/plugins/`: marketplace manifests
