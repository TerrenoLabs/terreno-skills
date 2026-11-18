# CHECKLIST.md template

Write this file at the app's repository root in the handoff stage. Replace
every `<...>`. Tick a box only when you ran the check and it passed. Keep each
item to something the owner can confirm in under two minutes.

```markdown
# <App Name> launch checklist

Built with Terreno <version> on <date>. Status of each stage is in
`.terreno/bootstrap.json`; rough edges are in `BOOTSTRAP_NOTES.md`.

## Get in

- Web app: <URL, or "run `bun run dev` in backend/ and `bun run web` in frontend/, then open http://localhost:8082">
- Initial admin: `<email>`. The password is `INITIAL_ADMIN_PASSWORD` in `<file or secret store>`.
- [ ] Sign in as the initial admin and change the password.

## 1. App runs
- [x] Backend health check is green (`<command>`)
- [x] Seeded users can sign in locally

## 2. <Feature name>
- [x] Add, edit, complete, and delete a <thing>
- [x] Another account cannot see my <things>
- [x] Works offline and syncs on reconnect

## 3. Sign-in security
- [x] No secrets committed; production refuses placeholder secrets
- [x] Password reset works
- [ ] Connect a real mail provider (`<variable>`) so reset and verification mail is delivered

## 4. Roles
- [x] Roles: <list>. One seeded user per role (see the seed script)

## 5. Admin
- [x] Admin panel at `/admin` lists and edits <things> and users
- [x] Non-admins are turned away

## 6. Look and layout
- [x] Brand colors: <primary>, <accent>. Change them in `frontend/constants/theme.ts`
- [x] Phone and desktop screenshots in `docs/bootstrap/theme/`
- [ ] Replace the placeholder icon and splash image

## 7. Assistant
- [ ] Set `<PROVIDER_KEY>` to turn the assistant on  <!-- blocked: no key -->

## 8. Consent
- [x] New users accept Terms and Privacy before the first screen
- [ ] Replace the placeholder Terms and Privacy text after legal review

## 9. Feature flags
- [x] `<flag>` controls <capability>; toggle it in the admin

## 10. Tests and CI
- [x] `<backend test command>` and `<frontend test command>` pass; coverage floor <n>%
- [x] GitHub Actions green on <commit>
- [ ] Connect the repository in CircleCI so `.circleci/config.yml` runs

## 11. Agent tooling
- [x] `CLAUDE.md`, `AGENTS.md`, MCP config, and Terreno skills are committed

## 12. Deploy
- [ ] <"Deployed at <URL>" or the exact credentials and commands needed>

## 13. Handoff
- [x] Initial admin `<email>` signs in; the password is in `<file or secret name>`
- [x] A fresh clone reaches a running app by following `README.md`

## Before real users
- [ ] Remove the development seed users from production
- [ ] Custom domain and HTTPS
- [ ] Database backups
- [ ] Error monitoring (`<variable>`)
```
