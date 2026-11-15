# Bootstrap stages

Read one section, do that stage, run its exit check, write the state entry.
Doc paths are relative to `docs/` in the Terreno repository at the installed
version's tag.

Every section has the same four parts:

- **Goal:** what is true when the stage is done.
- **Starts with:** what earlier stages or the scaffold already provide. Check
  it is really there before building on it.
- **Do:** the work, with the docs and skills to follow.
- **Exit check:** what you run and observe. All of it, not a sample.

---

## 1. scaffold

**Goal:** the generated app runs locally and a seeded user can sign in.

**Starts with:** an empty directory, Bun, and a MongoDB replica set (a
single-node replica set is fine; a standalone `mongod` is not, because sync
uses change streams).

**Do:**

1. `bunx create-terreno-app <app-name> --display-name "<App Name>"`. Pick the
   kebab-case name from the request ("a todo app" → `todo-app`). Pin a version
   with `create-terreno-app@<version>` when the user named one.
   The CLI writes into a new `<app-name>/` directory under the current one;
   that directory is the app root for every later stage.
2. `git init` in the app root if it is not a repository, and commit the
   untouched scaffold first so later diffs show only your work. The scaffold's
   `.gitignore` may ignore `.terreno/`; change it so `.terreno/bootstrap.json`
   is tracked and the rest stays ignored. Ignore the dev servers' log files
   and `.expo/` too.
3. Install in `backend/` and `frontend/`, start MongoDB, run the seed, start
   both processes. Follow `how-to/create-a-terreno-app.md` and the generated
   `README.md`, in that order. Wait for `/health` before any command that
   calls the backend (the SDK generator, the seed check).
4. If lint fails on the untouched scaffold, fix it with the package's own
   `lint:fix` and note it; do not disable rules to get to green.
5. Record the installed `@terreno/api` version as `terrenoVersion` in the
   state file.

**Exit check:**

- `GET /health` on the backend reports healthy.
- On the web app, the seeded admin signs in and lands on the first screen.
- Lint and the typecheck script (`compile` in a generated app) pass in both
  packages.

---

## 2. feature

**Goal:** the feature the user asked for works, local-first, scoped to its
owner. For "a todo app": todos with a title, a completed state, and an
optional due date; add, edit, complete, delete, and filter by open or done.

**Starts with:** the scaffold's user model, sync and realtime plugins, and an
empty first tab.

**Do:**

1. Model with a `description` on every field and the sync plugins
   (`how-to/create-a-model.md`; skills `terreno-backend-api`,
   `mongoose-schema-safety`).
2. `modelRouter` with owner permissions, an owner query filter, and a `sync`
   scope. No hand-written Express routes; custom endpoints are model router
   actions.
3. Regenerate both SDK files: the request hooks and the synced collection
   hooks (`how-to/generate-the-client-sdk.md`, `reference/syncdb.md`). If the
   scaffold has no script for the synced collection hooks, add one and pass
   the generated collection list to the sync client. A skill that mentions
   `@terreno/rtk` or Redux describes Terreno 57 or older: on 58 and later,
   follow the docs instead and note it.
4. Screens from `@terreno/ui` components, reading and writing through the
   synced collection hooks (`how-to/use-syncdb-correctly.md`,
   `how-to/build-list-detail-screens.md`; skills `terreno-ui`,
   `terreno-data-fetching`). Every screen has a loading, an empty, and an error
   state, and a `testID` on each interactive element. Give a new record its
   id on the client when you create it, so a record made offline can be
   edited and deleted before the server has seen it.
5. Seed a few example records for the seeded users.

**Exit check:**

- Create, edit, complete, and delete each survive a page reload.
- A second seeded user signs in and sees none of the first user's records;
  a direct API read of the first user's record as the second user is 403 or 404.
- With the network off, a change shows immediately and is on the server after
  the network returns.

---

## 3. auth

**Goal:** sign-in is safe to expose to the internet.

**Starts with:** Better Auth email and password, a login and sign-up screen,
and a security settings screen from the scaffold.

**Do** (`how-to/configure-better-auth.md`, `explanation/authentication.md`,
`reference/account-security.md`, `how-to/password-reset.md`,
`how-to/rate-limiting.md`):

1. Generate a random `BETTER_AUTH_SECRET` (and any other secret the env example
   lists) into the gitignored `.env`. No secret has a default in code.
2. Password reset and email verification work end to end. The scaffold sends
   no mail and has no reset or verification screens: add the mail package
   (`reference/comms.md`), pass its sender to the auth config, and add the
   screens the mailed links open. Without a mail provider, write development
   mail to a gitignored local file so a developer can open the link, wire the
   production provider from environment variables, and say in the notes that
   it was not exercised.
   Use one password rule in the sign-up form and the server.
3. Rate limiting stays on outside tests; set the proxy trust the deploy target
   needs. The auth bucket is small: restart the backend between full browser
   passes over sign-up, verify, and reset rather than raising the limit.
4. Decide sign-up: open for a consumer app, closed for an internal tool. A
   todo app is open.
5. Turn on two-factor in the security settings screen when the installed
   version supports it.
6. Production refuses to start with a missing or placeholder secret, and the
   seed refuses to create the default-password users when `NODE_ENV` is
   `production`.

**Exit check:**

- `grep` of committed files finds no secret value and no default password
  outside the seed's development-only users.
- A reset link sets a new password, and the old one stops working.
- Repeated bad logins are rejected with 429.
- An unauthenticated request to a data route is 401.

---

## 4. roles

**Goal:** at least one role between "any user" and "admin", enforced on the
server.

**Starts with:** the scaffold's `backend/src/access.ts` and default roles.

**Do** (`reference/api.md` permissions and access sections,
`reference/account-security.md`):

1. List the roles the scaffold already seeds before naming any; do not reuse
   one of their names for something else. Then name the roles the app needs.
   A todo app: `member` (own todos) and `support` (can read any user's todos,
   cannot edit them), plus the built-in admin roles.
2. Enforce through permissions on routers and actions, never in the client
   alone.
3. Hide controls the current role cannot use; the server check stays.
4. Seed one user per role.

**Exit check:**

- As `member`, a request for the support-only route is refused (403, or the
  status the installed version documents for a refused action).
- As `support`, the same request succeeds and a write to someone else's
  record is refused.
- A backend test covers both.

---

## 5. admin

**Goal:** an admin can manage the app's data and users from the admin panel.

**Starts with:** the scaffold's admin backend plugin and an admin index
screen. Check what is really there before building on it: on 58.0 the index
screen lists models but has no per-model routes, the admin plugin is
registered without the app's access control, and the role-management routes
are not mounted.

**Do** (`how-to/admin-add-model.md`, `how-to/build-admin-screens.md`; skill
`building-admin-interfaces`):

1. Make the admin and the roles from stage 4 agree first: one rule decides
   who may open the admin, and the server and the navigation both use it.
   Give the admin plugin the app's access control, and grant each admin model
   to the roles that should see it.
2. Build the admin shell the way `how-to/build-admin-screens.md` describes
   (provider, shell layout, home, and per-model list and form routes), not on
   top of the scaffold's index screen.
3. Register the feature's model in the admin with useful list fields and a
   default sort. Hide internal fields (password hashes, sync bookkeeping).
4. Keep the admin entry point out of the navigation for non-admins and
   redirect them if they type the URL. A reload on an admin URL must stay
   there for an admin.
5. Let an admin give and remove the roles from stage 4 in the admin, so the
   seed is not the only way to hold one.

**Exit check:**

- The admin lists the feature's records, edits one, and the change shows in
  the owner's app.
- A non-admin user cannot open the admin screens and is refused by every
  admin API route (403, or the status the installed version documents).
- An admin gives another user a role in the admin, and that user can then do
  what the role allows.

---

## 6. theme

**Goal:** the app looks like a product, not a scaffold, on a phone and on a
laptop, in light and dark.

**Starts with:** the scaffold's `frontend/constants/theme.ts` and the
`TerrenoProvider`.

**Do** (`reference/ui.md` theming and theme modes,
`explanation/responsive-design.md`; skills `terreno-ui`,
`audit-color-schemes`, `building-terreno-apps`):

1. Choose a brand: a primary and an accent color, set as theme primitives.
   Take them from the request when it names any; otherwise pick a restrained
   pair and note it. Set the app name, icon color, and splash to match.
2. No hard-coded hex colors in screens; use theme tokens through component
   props.
3. Lay out for width with the responsive props and breakpoint tokens: one
   column on a phone, a list and detail or a centered max-width column on
   desktop. No raw pixel cutoffs.
4. Offer light, dark, and follow-system in the profile screen.
5. Check contrast in both schemes.

**Exit check:**

- Screenshots of the sign-in screen, the main screen with data, and the main
  screen empty, at 390 and 1280 wide, light and dark (twelve images) in
  `docs/bootstrap/theme/`.
- Nothing overflows horizontally at 390 wide, and no control is smaller than a
  thumb can hit.
- Body text meets 4.5:1 contrast in both schemes.

---

## 7. ai

**Goal:** an assistant in the app that can answer about, and act on, the
user's own data.

**Starts with:** nothing; the scaffold does not include the AI package.

**Do** (`reference/ai.md`, `how-to/add-gpt-chat-mascot.md`,
`how-to/observe-llm-calls.md`; skill `ai-prompt-governance`):

1. Add `@terreno/ai` to the backend with one provider model read from an
   environment variable. With no key set, the server still starts and the chat
   screen says the assistant is not configured.
2. Add the chat screen with the UI library's chat component, history, and
   streaming.
3. Give the assistant at least one tool over the feature's data (for a todo
   app: list my open todos, add a todo), running as the signed-in user.
4. Keep prompts in named constants.
5. Add a backend test with a mock model.

**Exit check:**

- With a provider key: a streamed reply appears in the chat, a tool call
  creates a real record, and the request is in the AI request log.
- Without a key: the mock-model test passes and the stage is `blocked`, naming
  the variable.

---

## 8. consent

**Goal:** a new user accepts the terms and the privacy policy before using the
app, and the acceptance is stored.

**Starts with:** nothing wired in the frontend; read
`explanation/consent-forms.md` first.

**Do** (`explanation/consent-forms.md`, `reference/admin-backend.md` and
`reference/admin-frontend.md` consent sections):

1. Register the consent plugin and seed two published forms: Terms of Service
   and Privacy Policy, with short plain-language placeholder text marked as
   needing legal review.
2. Gate the app on outstanding consents after sign-in.
3. Expose consent forms and responses in the admin.

**Exit check:**

- A newly signed-up user sees both forms before the first screen and cannot
  skip them.
- After accepting, a reload goes straight to the app, and the responses are
  visible to an admin.
- Publishing a new version of a form asks the same user again.

---

## 9. flags

**Goal:** one real capability is behind a feature flag that an admin can turn
on without a deploy.

**Starts with:** whatever flag support the scaffold registered; check before
adding.

**Do** (`how-to/add-feature-flags.md`, `reference/feature-flags.md`):

1. Put the assistant from stage 7 (or, when it is blocked, another finished
   capability) behind a flag, checked on the server and in the client.
2. Read the release notes for the installed version (`terreno docs notes`, or
   the changelog at the version's tag). If the release added a capability that
   suits this app, adopt it behind a second flag and name it in the notes.

**Exit check:**

- Flag off: the entry point is absent and the route refuses.
- An admin turns it on, and a signed-in client shows the entry point without a
  reload or a redeploy.

---

## 10. tests-ci

**Goal:** the suites that protect the app run locally and in CI, with a
coverage floor that fails the build.

**Starts with:** two GitHub Actions workflows from the scaffold (backend,
frontend).

**Do** (`how-to/set-up-app-tests.md`, `how-to/github-actions-ci.md`; skills
`terreno-test-setup`, `terreno-backend-tests`, `terreno-frontend-tests`,
`backend-test-env`):

1. Backend tests for the feature's permissions, roles, and actions. Frontend
   tests for the main screen's states. One Playwright flow: sign in, add an
   item, complete it.
2. A coverage threshold in each package's test config, set to the measured
   coverage rounded down to the nearest five and never below 70 for backend
   lines. CI fails below it.
3. GitHub Actions: lint, typecheck, test with coverage, and the Playwright
   flow. Every workflow validates the secrets it needs before using them.
4. CircleCI: a `.circleci/config.yml` running the same commands, valid under
   `circleci config validate` when the CLI is present.
5. Push and watch the runs when the repository has a remote.

**Exit check:**

- Every suite passes locally; paste the summary lines into the state evidence.
- Coverage is at or above the floor, and lowering it by deleting a test makes
  the command fail.
- With a remote: the GitHub Actions runs are green on the pushed commit.
  CircleCI green when the project is connected, otherwise `blocked` for that
  half with the connection step in the checklist.

---

## 11. agent-tooling

**Goal:** the next coding agent that opens this repository is productive in
its first minute.

**Starts with:** the scaffold's `.mcp.json`, `.cursor/mcp.json`,
`.cursorrules`, and `CLAUDE.md`.

**Do** (`how-to/set-up-terreno-mcp.md`, `how-to/install-agent-skills.md`,
`how-to/debug-with-mcp.md`):

1. Install the Terreno skills into the repository
   (`npx skills add TerrenoLabs/terreno-skills`) and commit them.
2. Bring `CLAUDE.md` and `AGENTS.md` up to date with what this app now has:
   its models, roles, flags, test commands, and the smoke command.
3. Confirm both MCP servers start with the committed config and that the
   local one can read this app's logs and database.

**Exit check:**

- A docs search returns results through the hosted server or the CLI.
- With the app running, the last backend error and a database read come back
  through the local server or the CLI.
- `CLAUDE.md` names the test and lint commands, and they are the ones that
  work.

---

## 12. deploy

**Goal:** the app is reachable at a public URL with production settings.

**Starts with:** the scaffold's `Dockerfile` and env examples.

**Do** (`explanation/deployment-baseline.md`; then skill `deploy-gcp` with
`how-to/deploy-to-gcp.md`, or skill `deploy-vercel` with
`how-to/deploy-to-vercel.md`):

1. Use the target the user named. Otherwise use whichever target has
   credentials present; with neither, do the local half below and mark
   `blocked`.
2. Production database, secrets in the host's secret store, sign-up policy and
   proxy trust from stage 3, CORS and auth origins set to the deployed web
   origin.
3. Add a deploy workflow that runs after CI on the default branch.
4. Run the seed's initial-user step against production (stage 13 defines it).

**Exit check (deployed):** the root URL loads, a deep link loads on refresh,
sign-in works against the deployed backend, and the sync socket connects.

**Exit check (no credentials):** the production image builds and boots
against a local replica set with `NODE_ENV=production`, the web export builds
with a production API URL, and the stage is `blocked` naming the missing
credentials.

---

## 13. handoff

**Goal:** the user knows what they have, how to get in, and what only they can
finish.

**Starts with:** the state file and `BOOTSTRAP_NOTES.md`.

**Do:**

1. **Initial user.** Add a seed step that creates one admin from
   `INITIAL_ADMIN_EMAIL` and `INITIAL_ADMIN_PASSWORD`, idempotently, allowed
   in production. Locally, generate a random password into the gitignored
   `.env`, run the step, and confirm the sign-in. Never print the password in
   a committed file; say which file holds it.
2. **`CHECKLIST.md`** at the repository root, from
   [`checklist-template.md`](checklist-template.md). One section per stage,
   each item a checkbox the user can verify in under two minutes, already
   ticked only where you proved it. Blocked stages list the exact steps to
   unblock. End with a "Before real users" section: legal review of the
   consent text, a real mail provider, a custom domain, backups, removing the
   development seed users.
3. **`README.md`:** what the app is, how to run it, how to test it, how to
   deploy it, and a link to the checklist.

**Exit check:**

- `CHECKLIST.md` has a section for each of the thirteen stages, and every
  ticked item matches a `pass` in the state file.
- The initial admin signs in locally (and on the deployed URL when there is
  one) with the generated password.
- A fresh clone, following only `README.md`, reaches a running app.
