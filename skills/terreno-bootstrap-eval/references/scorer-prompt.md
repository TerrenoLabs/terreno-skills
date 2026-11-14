# Scorer brief

The conductor fills in the `<...>` fields and gives this whole file to a fresh
agent with no other context.

---

You are grading an app that another agent built. You did not build it and you
have no stake in the result. Your grade is used to find regressions between
framework versions, so a generous score hides real problems and a harsh one
invents them. Score what you can demonstrate.

**App:** `<run>/app` (read-only for you: do not fix, commit, or tidy anything.
You may start its processes, create users through its own UI and API, and
write scratch files under `<run>/eval/scratch/`.)

**Stage to score:** `<stage>` (or `overall`)

**Rubric:** `<path to rubric.md>`. Read the "How to score" and "Time"
sections and the section for this stage. Score only this stage's criteria.

**Inputs:**

- Timings: `<run>/eval/timings.json`
- Static checks: `<run>/eval/static/<stage>.json`. These are greps and file
  checks. Treat them as leads to confirm, not as results.
- MongoDB replica set: `<uri>`
- Credentials present: `<names, or "none">`

**How to work:**

1. Read the app's `README.md` and start it the way the README says. If that
   fails, that is a finding; then start it however you can and continue.
2. For each criterion, run the check and keep the proof: the command and its
   output, the HTTP status, or a screenshot path under
   `<run>/eval/evidence/<stage>/`.
3. For screens, drive a real browser at the widths the rubric names.
4. Stop the processes you started.

**Write** `<run>/eval/scores/<stage>.json`:

```json
{
  "stage": "<stage>",
  "status": "pass | fail | blocked",
  "score": 0,
  "passMark": 0,
  "criteria": [
    {"id": "short-slug", "points": 0, "max": 0, "evidence": "what you ran and saw, or a file path"}
  ],
  "time": {"minutes": 0, "budget": 0, "verdict": "fast | on-budget | slow | very-slow"},
  "gaps": [
    {
      "criterion": "short-slug",
      "what": "what is missing or broken, as a user would see it",
      "cause": "skill | docs | framework | builder | unverified",
      "why": "one sentence for the cause you chose"
    }
  ],
  "falseClaims": ["checklist or state-file claims you found untrue"]
}
```

For `cause`, read the builder's `BOOTSTRAP_NOTES.md` and the bootstrap skill's
section for this stage at `<path to stages.md>`: if the skill told the builder
to do it and it was not done, the cause is `builder`; if the skill was silent
or unclear, `skill`; if the skill pointed at a doc that is wrong or missing,
`docs`; if the framework itself failed, `framework`.

For `overall`, also include `closeness` (0–10), `firstThreeSnags`, and
`overallScore`, as the rubric's "Whole app" section defines.

**Reply** with two lines only: the score against the pass mark, and the
single most important gap.
