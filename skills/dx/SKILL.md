---
name: dx
description: "Terreno developer-experience workflows in one skill: debug a running app with terreno-local MCP tools, bootstrap Bun, Playwright, and Maestro test setups and write backend, frontend, and mobile tests, propose manual regression cases and end-user guide pages, bootstrap an MCP server, and set up social login. Use when debugging a Terreno app, setting up or writing tests, backfilling regression suites or user guides, adding an MCP server, or adding Google, GitHub, or Apple sign-in."
---

<!-- GENERATED from bundles.json by .github/scripts/bundles.py. Do not edit here. -->

# Terreno terreno dx bundle

Debug a running app over MCP, set up and write backend, frontend, and mobile tests, backfill regression suites and user guides, and wire social login and MCP servers.

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
| `debug-with-mcp` | [references/debug-with-mcp/GUIDE.md](references/debug-with-mcp/GUIDE.md) | Standard way to debug and drive Terreno apps: use the terreno CLI (or the same tools over terreno-mcp-local) instead of guessing from code or pasted logs. Invoke for any bug, 500/403, wrong data, crashes, empty screens, sync/offline issues, auth/storage problems, or verifying a fix on web or native. Use debug-syncdb-with-mcp when the failure is SyncDB outbox/conflicts/cursors only. |
| `terreno-test-setup` | [references/terreno-test-setup/GUIDE.md](references/terreno-test-setup/GUIDE.md) | Bootstrap or repair the test setup of a Terreno app: backend Bun tests with in-memory Mongo, frontend Bun + React Native Testing Library unit tests and Playwright web E2E, and mobile Maestro flows on iOS/Android. Use when an app has no tests yet, `bun test` finds nothing or crashes on import, a new backend/frontend/mobile package needs tests, or CI needs a test job or sharding. Not for writing individual tests — use terreno-backend-tests, terreno-frontend-tests, or terreno-mobile-tests. |
| `terreno-backend-tests` | [references/terreno-backend-tests/GUIDE.md](references/terreno-backend-tests/GUIDE.md) | Write and fix Bun tests for a Terreno backend: modelRouter routes and actions, permissions, Mongoose models and hooks, services that call SendGrid / Twilio / Expo push / Cloud Tasks / GCS / AI models, env-dependent code, time, and async side effects. Covers supertest + @terreno/test helpers, auth tokens, test data, service mocks, and flake-free waiting. Use when adding or changing backend behavior or when a backend test fails. If the app has no test preload yet, run terreno-test-setup first. |
| `terreno-frontend-tests` | [references/terreno-frontend-tests/GUIDE.md](references/terreno-frontend-tests/GUIDE.md) | Write and fix frontend tests for a Terreno Expo app: Bun + React Native Testing Library unit tests for components, screens, hooks, Redux/RTK and syncdb data, and Playwright web E2E for flows across screens and the backend. Covers renderWithTerreno, testID selectors, mocking data hooks without leaking module mocks, async waiting, and Playwright login/fixtures. Use when adding or changing frontend behavior or when a frontend test fails. If the app has no test preload or Playwright config, run terreno-test-setup first. |
| `terreno-mobile-tests` | [references/terreno-mobile-tests/GUIDE.md](references/terreno-mobile-tests/GUIDE.md) | Write and fix mobile tests for a Terreno Expo app on iOS and Android: Maestro flows that drive the native app on a simulator or emulator, and Bun unit tests for Platform.OS-specific code. Covers testID selectors on native, login subflows, waiting, platform branches, keyboards and system dialogs, reaching the local backend from a device, and debugging flaky flows. Use when a change affects native-only behavior (navigation gestures, push, deep links, permissions, keyboard, platform branches) or a Maestro flow fails. If the app has no Maestro setup, run terreno-test-setup first. |
| `backfill-regression` | [references/backfill-regression/GUIDE.md](references/backfill-regression/GUIDE.md) | Backfill a repository's manual regression suites. Survey the app for behavior that only a developer or QA can check by hand (push notifications and other hardware or OS behavior, real email or SMS delivery, full cross-device flows, how the app feels) plus a short check that the app works as intended, propose candidate cases one area at a time, and have the human approve, edit, or deny each set before anything is written. Loops until no candidates remain or the human stops. Use when asked to backfill, seed, or audit regression tests or a manual QA checklist; not for planning a feature (Grow writes those cases) or for writing automated tests. |
| `backfill-user-guide` | [references/backfill-user-guide/GUIDE.md](references/backfill-user-guide/GUIDE.md) | Backfill a repository's end-user guide. Survey the shipped app for user-facing features (screens, navigation, forms, settings, admin tools) that have no guide page, draft pages in the user-guide format one area at a time, and have the human approve, edit, or deny each set before anything is written. Loops until every shipped feature has a page or a recorded denial, or the human stops. Use when asked to backfill, seed, or audit the user guide, help pages, or "how do I" docs for chat agents; not for planning a feature (Grow plans those pages) or for developer docs. |
| `bootstrap-mcp-server` | [references/bootstrap-mcp-server/GUIDE.md](references/bootstrap-mcp-server/GUIDE.md) | Bootstrap a backend-only Terreno MCP server that ships as a single Bun executable with the admin console embedded. Scaffolds the backend with create-terreno-app, drops the frontend, registers MCP tools, service tokens, optional MCP OAuth using the admin console's consent screen, a request log, tool on/off switches, and the MCP admin screens, then compiles everything (admin SPA included) into one binary. Trigger with "bootstrap an MCP server", "new Terreno MCP server", "MCP-only backend", or "ship the MCP server as a binary". Not for a full Expo app (use the terreno_bootstrap prompt / create-terreno-app) or for adding MCP tools to an existing app (see https://terreno-docs.netlify.app/how-to/expose-mcp-tools). |
| `set-up-social-login` | [references/set-up-social-login/GUIDE.md](references/set-up-social-login/GUIDE.md) | Set up Google, GitHub, and Sign in with Apple in a Terreno app on Better Auth: server config, callback URLs for local dev, previews, and the stable deploy, provider registration, secrets, trying the providers on one preview first, choosing same-site hosts, and checking the result. Use when asked to "add Google/Apple/GitHub login", "set up social login" or OAuth, "register the OAuth callbacks", "point OAuth at the preview", or when a social sign-in fails with a redirect mismatch. Not for email/password, passkey, or 2FA setup alone (see configure-better-auth.md). |

## Installing a different slice

Every member also installs alone
(`npx skills add TerrenoLabs/terreno-skills --skill debug-with-mcp`), and `npx skills add TerrenoLabs/terreno-skills` opens a
picker grouped by the same bundles.
