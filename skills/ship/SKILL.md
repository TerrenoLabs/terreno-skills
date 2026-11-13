---
name: ship
description: "Terreno verify-and-ship workflows in one skill: verify UI changes in a running app, attach screenshots and videos to a PR, keep docs in sync, generate release announcements, upgrade Terreno, produce App Store and Play Store assets, and deploy to GCP (Cloud Run and static web). Use when asked to verify a frontend change, attach PR media, update docs, announce a release, upgrade Terreno, make store screenshots, or deploy."
---

<!-- GENERATED from bundles.json by .github/scripts/bundles.py. Do not edit here. -->

# Terreno verify and ship bundle

UI verification, PR evidence, docs, releases, upgrades, store assets, and GCP deploys.

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
| `verify-ui-changes` | [references/verify-ui-changes/GUIDE.md](references/verify-ui-changes/GUIDE.md) | Mandatory when any feature touches the frontend. Launch the app, log in, exercise the feature, save screenshots/videos, and post evidence to the PR. Lifecycle composition: Pick for implementation runtime checks, Roast for independent proof, and Taste after a UI-affecting review/CI fix. |
| `attach-pr-media` | [references/attach-pr-media/GUIDE.md](references/attach-pr-media/GUIDE.md) | Upload screenshots or videos from a local path to GitHub and embed them in a pull request comment or body, using only the gh CLI token (no browser). Use after verify-ui-changes captures evidence, or when asked to "attach screenshots to the PR", "upload images to GitHub", or "put the recording on the PR". Also use when /opt/cursor/artifacts/ is missing or read-only. |
| `update-docs` | [references/update-docs/GUIDE.md](references/update-docs/GUIDE.md) | Keep Terreno docs in sync whenever behavior, public API, architecture, or operator workflow changes. Read architecture docs first; write Diátaxis pages in the same slice; regenerate generated docs. Lifecycle composition: Pick when behavior and docs change together; Roast proves docs; Brew is the final docs gate. |
| `generate-release-announcements` | [references/generate-release-announcements/GUIDE.md](references/generate-release-announcements/GUIDE.md) | Generate, validate, and optionally upload a multi-announcement Markdown release pack for @terreno/announcements. Use when asked to announce a product release, turn release notes or a Linear Release into in-app announcements, create an announcement pack, or upload release announcements as drafts or live. |
| `upgrading-terreno` | [references/upgrading-terreno/GUIDE.md](references/upgrading-terreno/GUIDE.md) | Upgrade Terreno lockstep @terreno/* packages. Trigger with "upgrade Terreno", "bump @terreno packages", "update to the latest Terreno", or "upgrade terreno version". |
| `store-assets` | [references/store-assets/GUIDE.md](references/store-assets/GUIDE.md) | Produce App Store and Google Play listing assets for an Expo app: store-sized screenshots (6.5-inch iPhone, 13-inch iPad, 1080x1920 Android phone) captured by Maestro flows that log in with test accounts, the Play feature graphic (1024x500 banner), and the Play high-res icon (512x512). Also keeps a simulator/emulator Expo dev client in sync with the native fingerprint (checks EAS, downloads a matching build, or starts one). Use when the user asks for "store screenshots", "App Store / Play Store screenshots", "store listing assets", "feature graphic", "store banner", "Play Store icon", "512 icon", or to launch an app in the simulator/emulator with an up-to-date dev client. |
| `deploy-gcp` | [references/deploy-gcp/GUIDE.md](references/deploy-gcp/GUIDE.md) | Deploy a Terreno app to GCP — Cloud Run backend and GCS+CDN static web. Trigger phrases include "deploy to GCP", "deploy to Cloud Run", and "ship the backend". |

## Installing a different slice

Every member also installs alone
(`npx skills add TerrenoLabs/terreno-skills --skill verify-ui-changes`), and `npx skills add TerrenoLabs/terreno-skills` opens a
picker grouped by the same bundles.
