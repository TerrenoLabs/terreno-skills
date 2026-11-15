# Scoring rubric

For the scorer only. The builder must never see this file.

## How to score

- Verify by running: start the app, call the API, drive the browser, run the
  test command. Reading the code is for finding where to look, not for
  awarding points.
- Each criterion is all or nothing unless it says "partial". If you could not
  run the check, the criterion scores 0 and the reason goes in `gaps` with
  `cause: "unverified"`.
- Ignore the builder's claims in the state file, the checklist, and commit
  messages. A ticked checklist item you find false is a 5-point penalty on the
  `handoff` stage, once per item.
- A stage the state file marks `blocked` for missing credentials: score the
  criteria tagged **(local)**, report `status: "blocked"`, and scale the local
  points to the stage's full weight for the overall total only when every
  local criterion passed. Otherwise use the raw points.

Each stage is scored out of 100, then weighted into the overall score.

## Time

Budgets are for the builder's wall time on one attempt, on a warm machine
(dependencies cached). Record the verdict per stage and overall.

| Stage | Budget (min) | Stage | Budget (min) |
| --- | --- | --- | --- |
| scaffold | 10 | consent | 15 |
| feature | 25 | flags | 10 |
| auth | 20 | tests-ci | 30 |
| roles | 15 | agent-tooling | 10 |
| admin | 10 | deploy | 30 |
| theme | 25 | handoff | 10 |
| ai | 25 | **Total** | **235** |

Verdict: `fast` (≤ 60% of budget), `on-budget` (≤ 100%), `slow` (≤ 200%),
`very-slow` (> 200%). Time does not change a stage's score; it is reported
beside it. In the overall score, time is its own 10-point line: 10 for a total
on budget, 5 for up to 200%, 0 beyond. Count the first attempt for the
verdict and report retries separately.

## Stages

Weight is the stage's share of the quality part of the overall score; the
weights sum to 100.
Pass mark is the score below which the conductor runs a fix round.

### scaffold — weight 6, pass mark 90
- 30 Backend starts and `/health` reports healthy
- 30 Web app loads and a seeded user signs in
- 15 Lint and typecheck pass in both packages
- 15 State file exists with the Terreno version and this stage's entry
- 10 The untouched scaffold is its own first commit

### feature — weight 12, pass mark 80
- 20 Create, edit, complete, delete all work in the browser and survive reload
- 15 Second user cannot list or read the first user's records (API-level)
- 15 Offline change appears immediately and reaches the server on reconnect
- 10 Open/done filter works
- 10 Loading, empty, and error states exist (partial: 3 each, 10 for all)
- 10 Data goes through the synced collection hooks; no raw `fetch`/`axios` in screens; generated SDK files are unedited
- 10 Every model field has a description; no hand-written Express routes
- 10 Interactive elements have `testID`s

### auth — weight 10, pass mark 80
- 20 No secret values or default passwords committed (outside dev-only seed users)
- 15 Production start fails on a missing or placeholder secret
- 15 Password reset works end to end
- 10 Email verification flow exists and works with development delivery
- 15 Repeated bad logins return 429
- 10 Unauthenticated data requests return 401
- 10 Seed refuses default-password users in production
- 5 Two-factor available in security settings (0 if the version lacks it and the notes say so: award 5)

### roles — weight 7, pass mark 75
- 25 A role exists between ordinary user and admin, defined on the server
- 25 Ordinary user is refused on the privileged route (403, or 405 where the version documents that for a refused action)
- 20 Privileged role succeeds on it and is refused a write it should not have
- 15 A backend test covers both and passes
- 15 One seeded user per role; UI hides controls the role cannot use

### admin — weight 7, pass mark 80
- 30 Admin lists the feature's records with sensible columns
- 25 Admin edits a record and the owner sees the change
- 25 Non-admin is refused by the admin API (403) and redirected from the admin screens
- 10 Users are manageable in the admin, including giving and removing a role
- 10 Admin link is absent from navigation for non-admins

### theme — weight 10, pass mark 75
- 15 A brand palette is set through theme primitives, not the scaffold default
- 15 No hard-coded hex colors in screens
- 20 At 390 wide: no horizontal overflow, controls reachable, on sign-in, main, and empty screens
- 15 At 1280 wide: layout uses the space deliberately (max width or list/detail), not a stretched phone column
- 15 Light, dark, and follow-system selectable; both schemes legible (4.5:1 body text)
- 10 Twelve screenshots present and matching the running app
- 10 Looks like a product: consistent spacing, a real empty state, named app and icon color (judge from your own screenshots; partial 0/5/10)

### ai — weight 8, pass mark 70
- 20 **(local)** Server starts without a provider key; chat screen says the assistant is not configured
- 20 **(local)** Mock-model backend test passes
- 15 **(local)** At least one tool over the user's own data, running as that user
- 10 **(local)** Prompts are named constants
- 20 With a key: streamed reply renders in the chat
- 15 With a key: a tool call creates a real record and the request is logged

### consent — weight 7, pass mark 75
- 30 New user is shown Terms and Privacy before the first screen and cannot skip
- 20 Acceptance persists across reload and is stored on the server
- 20 Publishing a new version re-prompts
- 15 Forms and responses visible in the admin
- 15 Placeholder legal text is clearly marked for review

### flags — weight 5, pass mark 75
- 35 Flag off: entry point absent and the server route refuses
- 35 Admin turns it on; a signed-in client updates without reload or redeploy
- 15 Release notes for the version were consulted; the notes say what was adopted or why nothing was
- 15 Flag is documented in the agent docs or README

### tests-ci — weight 10, pass mark 80
- 20 **(local)** Backend and frontend suites pass locally
- 15 **(local)** Coverage floor configured in both packages; backend lines ≥ 70; breaking it fails the command
- 10 **(local)** One Playwright flow exists and passes locally
- 10 **(local)** `.circleci/config.yml` exists and runs the same commands (valid under `circleci config validate` when available)
- 10 **(local)** Workflows validate required secrets before use
- 25 GitHub Actions green on the uploaded commit
- 10 CircleCI green on the uploaded commit

### agent-tooling — weight 5, pass mark 80
- 25 MCP config committed and both servers start with it
- 25 Terreno skills installed and committed
- 25 `CLAUDE.md` and `AGENTS.md` describe this app (models, roles, flags, commands) and the commands work
- 25 Docs search, last backend error, and a database read all work through the CLI or the local server

### deploy — weight 8, pass mark 70
- 20 **(local)** Production image builds and boots against a replica set with `NODE_ENV=production`
- 15 **(local)** Web export builds with a production API URL
- 10 **(local)** A deploy workflow exists and validates its secrets
- 20 Root URL loads and a deep link loads on refresh
- 20 Sign-in works against the deployed backend
- 15 Sync socket connects on the deployed app

### handoff — weight 5, pass mark 85
- 25 `CHECKLIST.md` at the root, a section per stage, items checkable in two minutes
- 20 Ticked items are true (penalties above apply)
- 20 Initial admin is created by an idempotent seed step from environment variables and can sign in
- 10 The initial password is not in any committed file, and the checklist says where it is
- 15 Blocked stages list exact unblocking steps; a "Before real users" section exists
- 10 A fresh clone following only the README reaches a running app

## Whole app

Scored once at the end, as the beginner who typed the prompt:

- **Closeness (0–10, reported, not added to the total):** how much of what
  they literally asked for can they do right now, without reading code?
  10 = signs in, has their own todos, finds the admin, it looks right on a
  phone and a laptop, and it is online.
- **First three snags:** the first three things that would confuse or stop
  them, in the order they would hit them.
- **Overall score (0–100):** quality is `sum(stage score × weight) / 100`
  (the weights sum to 100), scaled by 0.9, plus the time line out of 10.
