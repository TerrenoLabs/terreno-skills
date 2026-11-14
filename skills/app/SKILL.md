---
name: app
description: "Terreno app-building conventions in one skill: @terreno/api backends and modelRouter, @terreno/ui screens, light/dark mode and color-contrast audits, data fetching and SyncDB, SDK generation, Mongoose schema and index safety, admin interfaces, backend test env, and AI prompt governance. Use when adding or changing models, routes, screens, forms, network requests, schemas, indexes, admin tools, or prompts in a Terreno app, or when debugging SyncDB state."
---

<!-- GENERATED from bundles.json by .github/scripts/bundles.py. Do not edit here. -->

# Terreno terreno apps bundle

Backend, UI, light/dark mode, data, schema, admin, and test conventions for building Terreno apps.

This skill bundles 12 Terreno skills into one install. Each member is a
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
| `building-terreno-apps` | [references/building-terreno-apps/GUIDE.md](references/building-terreno-apps/GUIDE.md) | Complete guide for building Terreno full-stack Expo apps with @terreno/ui, Expo Router, and @terreno/rtk. Covers layout, forms, navigation, theming, screen patterns, and when to use Expo Go vs custom builds. |
| `terreno-backend-api` | [references/terreno-backend-api/GUIDE.md](references/terreno-backend-api/GUIDE.md) | Guidelines for creating backend APIs with @terreno/api on Express/Mongoose. Covers when to use Terreno backend vs Expo API routes, modelRouter CRUD, permissions, modelRouter actions (not app.get/app.post), OpenAPI generation, and the SDK codegen pipeline. Use when adding models, routes, auth, or server-side logic in Terreno apps. Lifecycle composition: Grow for API shape, Pick for implementation, Roast for API/integration proof. |
| `terreno-ui` | [references/terreno-ui/GUIDE.md](references/terreno-ui/GUIDE.md) | Build UI with @terreno/ui — Terreno's React Native component library with a large component set and a three-layer theming system. Use when adding or reviewing layout, forms, tables, modals, feedback, or navigation chrome. Covers component selection, Box/Page patterns, theme props, and when NOT to use raw React Native primitives. Lifecycle composition: Grow for UI shape, Pick for implementation, Roast for UI conformance review. Not for backend APIs, RTK Query, or Expo Router setup. |
| `audit-color-schemes` | [references/audit-color-schemes/GUIDE.md](references/audit-color-schemes/GUIDE.md) | Audit a Terreno app's light and dark mode support: find every hardcoded color and theme.primitives read, move each to a semantic @terreno/ui theme token, and prove what stays fixed meets WCAG 2.2 AA contrast against the app's own light AND dark surfaces (static scan, resolved-theme contrast matrix, axe scan of rendered pages in both modes). Use when asked to audit or fix dark mode, light mode, theming, color tokens, hardcoded colors, or color contrast across an app, or before shipping dark mode. Not for one changed screen's accessibility gate (use accessibility-testing) or building new UI (use terreno-ui). |
| `terreno-data-fetching` | [references/terreno-data-fetching/GUIDE.md](references/terreno-data-fetching/GUIDE.md) | Use when implementing or debugging ANY network request, API call, or data fetching in a Terreno app. Covers syncdb collection CRUD, RTK Query generated hooks for non-synced routes, admin's host-bound fetch client, auth, caching, and SDK regeneration. Replaces direct fetch, axios, React Query, and SWR in application code. Lifecycle composition: Grow for data-flow shape, Pick for implementation, Roast for independent network/cache behavior proof. |
| `generate-sdk` | [references/generate-sdk/GUIDE.md](references/generate-sdk/GUIDE.md) | Regenerate the example-frontend RTK Query SDK (store/openApiSdk.ts) from the example-backend's OpenAPI spec. Handles dependency install, backend startup, SDK codegen, and cleanup from a fresh checkout. Use whenever the backend's API surface changes — new modelRouter routes, custom routes registered via createOpenApiBuilder, new/modified Mongoose models or field descriptions in example-backend, changes to permissions/queryFields/populatePaths/responseHandler, edits to @terreno/api routing or OpenAPI generation, or any time a route is added/removed/renamed. Also use when the user asks to "regenerate the SDK", "update openApiSdk.ts", "run bun run sdk", or reports stale/missing generated hooks. Lifecycle composition: Pick after API-shape changes; Roast to verify generated-client compatibility. |
| `debug-syncdb-with-mcp` | [references/debug-syncdb-with-mcp/GUIDE.md](references/debug-syncdb-with-mcp/GUIDE.md) | Invoke when debugging SyncDB local state, stale data, outbox stalls, conflicts, cursor/stream drift, reconciliation, or offline behavior in a running Terreno app. Uses the terreno CLI (or terreno-mcp-local) to inspect, snapshot, compare, mutate, flush, merge, and repair SyncDB state. |
| `mongoose-schema-safety` | [references/mongoose-schema-safety/GUIDE.md](references/mongoose-schema-safety/GUIDE.md) | Invoke when making any Mongoose schema change: adding/removing/renaming fields, creating a new model, adding indexes, or writing a backfill migration. Provides the five-type pattern, risk matrix, type file checklist, and rollout safety steps for Terreno backends. |
| `mongo-index-review` | [references/mongo-index-review/GUIDE.md](references/mongo-index-review/GUIDE.md) | Review a PR, one API (model + router), or a whole package for the MongoDB queries it issues and recommend the indexes to add, change, or drop. Use when asked to review Mongo indexes, find slow or unindexed queries, check a PR's queries for index coverage, or when an architecture review touches Mongoose models. Read-only: reports recommendations, never edits schemas. |
| `building-admin-interfaces` | [references/building-admin-interfaces/GUIDE.md](references/building-admin-interfaces/GUIDE.md) | Build Terreno admin UIs with @terreno/admin-frontend and @terreno/admin-backend. Use when adding or changing admin screens, AdminShell sidebar nav, AdminHome, custom screens, AdminScreenRouter, AdminProvider widgets, admin-spa routes, or operator tools. Covers where models vs custom screens vs platform tools go. Not for product (non-admin) Expo screens — use building-terreno-apps. |
| `backend-test-env` | [references/backend-test-env/GUIDE.md](references/backend-test-env/GUIDE.md) | Invoke when writing tests that mutate `process.env` in `@terreno/api`, `@terreno/ai`, or `example-backend` — feature flags, auth secrets, integration toggles. Covers the preload contract, `setupEnvironment()`, and safe mutation patterns. Lifecycle composition: Pick when writing these tests; Roast when independently reproducing env-sensitive behavior. |
| `ai-prompt-governance` | [references/ai-prompt-governance/GUIDE.md](references/ai-prompt-governance/GUIDE.md) | Invoke when adding, modifying, or reviewing any prompt used by `@terreno/ai` (AIService methods, system prompts, helpers) or when shipping a new AI product feature (dataset, evaluators, experiments, production label, live feedback). Provides prompt-as-constant/registry rules, SOP loop, temperature presets, logging/tracing, and a testing checklist. Lifecycle: Grow for prompt-contract decisions, Pick for implementation, Roast for independent prompt-behavior verification. |

## Installing a different slice

Every member also installs alone
(`npx skills add TerrenoLabs/terreno-skills --skill building-terreno-apps`), and `npx skills add TerrenoLabs/terreno-skills` opens a
picker grouped by the same bundles.
