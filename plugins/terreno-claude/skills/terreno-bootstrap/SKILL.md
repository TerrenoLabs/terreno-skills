---
name: terreno-bootstrap
description: >-
  Take a new Terreno app from an empty directory to a deployed, production-shaped
  product in thirteen resumable stages: scaffold, first feature, secure auth,
  roles, admin, theme and responsive layout, AI chat, consent forms, feature
  flags, tests and CI with coverage, agent tooling, deploy, and a handoff
  checklist with an initial user. Use when asked to "make me an app with
  Terreno", "start a new Terreno project", "bootstrap a Terreno app", "build a
  todo app", or to run or resume one bootstrap stage. Not for adding a feature
  to an app that already shipped (use the app skills) or for work inside the
  Terreno monorepo.
metadata:
  internal: true
---
# Terreno bootstrap

Build a new Terreno app in stages. Each stage has one goal, an exit check you
run, and a line in the state file. A stage that passed is never redone; a run
can stop after any stage and resume later.

The request is often one sentence from someone who has never used Terreno
("make me a todo app with login"). Do not ask them to choose between framework
options they have not heard of. Build every stage below by default. Ask only
for what you cannot invent: the app's name when it is not given, and
credentials (see [Blocked is a result](#blocked-is-a-result)).

## Sources

Use the documentation that matches the installed Terreno version, not memory:

- Docs for a version: `https://github.com/TerrenoLabs/terreno/tree/<version>/docs`
  (tags are bare versions such as `58.0.6`). Start at `docs/README.md`.
- Hosted MCP (`terreno_search_docs`, generators) and the `terreno` CLI
  (`terreno docs search <query>`) when the project has them.
- The other Terreno skills named in each stage.

When the docs and this skill disagree, follow the docs for the installed
version and record the disagreement in `BOOTSTRAP_NOTES.md` at the app root.

## State

Keep `.terreno/bootstrap.json` at the app root, committed:

```json
{
  "app": "todo-app",
  "terrenoVersion": "58.0.6",
  "request": "the user's original words, verbatim",
  "stages": {
    "scaffold": {"status": "pass", "finishedAt": "2026-11-14T20:03:11Z", "evidence": "health 200; logged in as admin@example.com"},
    "deploy": {"status": "blocked", "reason": "no GCP or Vercel credentials"}
  }
}
```

`status` is `pass`, `fail`, `blocked`, or `skipped` (only when the user asked
for the stage to be left out). Write the stage's entry as soon as its exit
check is decided, then commit. One commit per stage, named for what the app
gained.

## Running stages

- **Whole bootstrap:** run the stages in order. Continue past a `blocked`
  stage; stop on a `fail` you cannot fix in three attempts and say which exit
  check is red.
- **One stage** ("run the theme stage", `stage=theme`): read the state file,
  confirm every earlier required stage is `pass` or `blocked`, run only that
  stage, write its entry, stop.
- **Resume:** run the first stage with no `pass`, `blocked`, or `skipped`.

Before a stage, read its section in [`references/stages.md`](references/stages.md).
It gives the goal, what the scaffold already provides, the docs to read, and
the exit check.

| # | Stage | The app gains | Exit check, in short |
| --- | --- | --- | --- |
| 1 | `scaffold` | Running backend, web app, seeded users | `/health` healthy; seeded admin logs in on web |
| 2 | `feature` | The requested feature, local-first | Create, edit, complete, delete survive a reload; another user cannot see them |
| 3 | `auth` | Hardened sign-in | No default secrets; reset and verification flows work; rate limit on |
| 4 | `roles` | Roles beyond admin / not admin | A non-privileged user gets 403 on a privileged route |
| 5 | `admin` | Admin panel over the app's models | Admin edits a record; normal user cannot open `/admin` |
| 6 | `theme` | Brand theme, light and dark, phone and desktop layouts | Screenshots at 390 and 1280 wide, both schemes, no overflow |
| 7 | `ai` | Assistant chat wired to the app's data | A streamed reply and a logged request, or `blocked` without a key |
| 8 | `consent` | Terms and privacy consent gate | New user must accept before the first screen; response is stored |
| 9 | `flags` | One capability behind a feature flag | Toggling the flag changes the UI without a redeploy |
| 10 | `tests-ci` | Tests, coverage floor, GitHub Actions and CircleCI | Suites pass locally with coverage at or above the floor; both CI configs valid |
| 11 | `agent-tooling` | MCP config, agent rules, installed skills | An agent in the repo can search docs and read the running app's logs |
| 12 | `deploy` | Public URL | Deployed login works and the socket connects, or `blocked` without credentials |
| 13 | `handoff` | `CHECKLIST.md`, initial user, README | Checklist covers every stage; the initial user can sign in |

## Rules for every stage

1. **Prove the exit check by running it.** Start the app and exercise the
   behavior; a compile is not proof. Save screenshots for any stage that
   changes a screen under `docs/bootstrap/<stage>/`.
2. **Keep the app green.** After each stage: lint, typecheck, and the tests
   that exist pass. A later stage never leaves an earlier exit check red.
3. **Regenerate, never hand-edit, generated files** (`store/apiSdk.ts`,
   `store/syncDbSdk.ts`). Use the `generate-sdk` skill after backend changes.
4. **No placeholder secrets in committed files.** Generate real random
   secrets into gitignored `.env` files; commit only `.env.example` with empty
   values and a comment saying how to make one.
5. **Record friction.** One line in `BOOTSTRAP_NOTES.md` whenever a doc was
   wrong, a command failed, or you had to guess. This file is how the next
   version of this skill and the docs get better.

## Blocked is a result

`ai` needs a model provider key. `deploy` needs hosting credentials. CircleCI
needs the project connected. When one is missing:

1. Build everything that does not need it (the code, the config, the workflow).
2. Verify what can be verified locally (a mock model, a production build that
   boots in a container).
3. Mark the stage `blocked` with the exact variable or permission that is
   missing.
4. Put the unblocking steps in `CHECKLIST.md` in the handoff stage.

Never mark a stage `pass` on a local stand-in, and never invent a URL, a key,
or a passing check.

## Done

The bootstrap is done when every stage is `pass`, `blocked`, or `skipped`,
`CHECKLIST.md` exists, and the final message tells the user, in this order:
how to open the app (URL or the two start commands), the initial user's email
and where its password is, and which checklist items need them.
