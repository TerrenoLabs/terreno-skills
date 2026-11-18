---
name: terreno-bootstrap-eval
description: >-
  Regression-test the terreno-bootstrap skill against a Terreno version: hand a
  fresh builder agent a one-sentence beginner prompt, run the bootstrap one
  stage at a time, time each stage, have a separate scorer agent grade the
  result against a hidden rubric, upload the app and scorecard to the results
  repository, compare with the previous version, then fix the skill and rerun
  the weak stages in a loop. Use when asked to "eval the bootstrap", "run the
  bootstrap regression", "score the todo app build", "test bootstrap on
  <version>", or after a Terreno minor or major release. Not for building a
  real app (use terreno-bootstrap).
metadata:
  internal: true
---
# Terreno bootstrap eval

Answers one question per Terreno version: **given what a beginner would type,
how close does `terreno-bootstrap` get, and how long does it take?** The
generated app is evidence. The scorecard, the timings, and the diff against
the previous version are the product.

Three roles, three separate agents. Keeping them apart is what makes the
number mean something:

| Role | Sees | Never sees |
| --- | --- | --- |
| **Builder** (fresh subagent per stage) | The beginner prompt, the `terreno-bootstrap` skill, the app directory | The rubric, the scorer's notes, this skill |
| **Scorer** (fresh subagent per scoring pass) | The rubric, the app directory, the timings, the static-check report | The builder's transcript or its claims beyond what is in the repository |
| **Conductor** (you) | Everything | — |

The conductor never edits the generated app and never scores it.

## Inputs

| Input | Default |
| --- | --- |
| `version` | Latest published `create-terreno-app` |
| `stages` | All thirteen, in order. `stages=theme,ai` runs a subset on an existing run |
| `prompt` | `default` from [`references/noob-prompt.md`](references/noob-prompt.md) |
| `results repo` | `TerrenoLabs/terreno-bootstrap-runs` |
| `max fix rounds` | 2 per stage, 6 per run |

Run it once for the latest patch of every minor and major release (58.0,
58.1, 59.0, ...). Patch releases only when one touched the scaffold or a stage
failed on the previous patch.

`SKILL_DIR` below is this skill's directory.

## Procedure

### 0. Set up the run

1. Pick a run id: `<version>-<UTC yyyymmddThhmm>`. Create an empty run
   directory outside any repository: `<run>/app/` for the builder and
   `<run>/eval/` for everything else. The builder is only ever told about
   `<run>/app/`. The scaffold stage creates the app in `<run>/app/<app-name>/`;
   from the second stage on, that directory is the app directory you give
   builders, scorers, and the scripts.
2. Record the environment in `<run>/eval/run.json`: version, run id, prompt
   id, the `terreno-skills` commit, the model each role runs on, and which
   credentials are present (names only, never values).
3. Make sure a MongoDB replica set is reachable and note its URI for the
   builder. Infrastructure the builder cannot be expected to conjure is the
   conductor's job; framework knowledge is not.

### 1. Stage loop

For each stage, in order:

1. `python3 SKILL_DIR/scripts/stage_timer.py start <run>/eval <stage>`
2. **Spawn a fresh builder** with exactly this brief, and nothing about the
   rubric or what will be checked:

   > Work in `<run>/app`. A user asked: "<the beginner prompt, verbatim>".
   > Use the `terreno-bootstrap` skill at `<path>` and run only its `<stage>`
   > stage, pinned to Terreno `<version>`. MongoDB replica set: `<uri>`.
   > Follow the skill; do not ask me questions. When the stage is done or
   > blocked, reply with one line: the stage status and the commit.

   The first stage's builder gets the same brief; the prompt is the only
   product direction any builder ever receives.
3. `python3 SKILL_DIR/scripts/stage_timer.py stop <run>/eval <stage> --status <pass|fail|blocked>`
   using the status from `.terreno/bootstrap.json`, not the builder's reply.
   Record builder token use when the host reports it:
   `--tokens <n>`.
4. `python3 SKILL_DIR/scripts/static_checks.py <app-dir> --stage <stage> --out <run>/eval/static/<stage>.json`,
   where `<app-dir>` is the app directory from setup (`<run>/app` also works:
   the script finds the one app repository inside it)
5. **Spawn a fresh scorer** with [`references/scorer-prompt.md`](references/scorer-prompt.md),
   filled in for this stage. It writes `<run>/eval/scores/<stage>.json`.
6. Decide:
   - Score at or above the stage's pass mark in the rubric → next stage.
   - Below, and a later stage depends on it → [fix round](#2-fix-round), then
     rerun this stage.
   - Below, and nothing depends on it → note it, continue, fix after the run.

A stage the builder marked `blocked` for missing credentials is scored on its
local half only and reported as `blocked`, never as a pass or a regression.

### 2. Fix round

The loop exists to improve the skill and the docs, not to coach one build
over the line.

1. Read the scorer's `gaps` for the stage and the builder's
   `BOOTSTRAP_NOTES.md`. Sort each gap into one cause:
   - **skill**: the stage's instructions were missing, vague, or wrong.
   - **docs**: the Terreno docs for this version were missing or wrong.
   - **framework**: the scaffold or a package is broken.
   - **builder**: the instructions were clear and the builder did not follow
     them.
2. For **skill** gaps, edit `terreno-bootstrap` on a branch of
   `terreno-skills`. Fix the instruction generally; never write the rubric's
   wording or this app's specifics into the skill. One commit per gap.
3. For **docs** and **framework** gaps, write an issue draft into
   `<run>/eval/issues/` (title, body, labels). Do not file it unless asked.
4. **builder** gaps get no fix. Two builder gaps on the same instruction in
   one run are a skill gap: the instruction is not landing.
5. Reset the app to the commit before the stage (`git reset --hard` inside
   `<run>/app` only), rerun the stage with a new builder, and time it as
   attempt 2. Keep every attempt's timing and score.

Stop fixing a stage after `max fix rounds`; record it as failing and move on.

### 3. Whole-app score

After the last stage, spawn one more scorer with the rubric's "Whole app"
section: start the app cold from the README, sign in as the initial user, walk
the checklist, and score how close the result is to what the beginner asked
for. It writes `<run>/eval/scores/overall.json`, including total wall time,
the time verdict, and the three things a beginner would hit first.

### 4. Publish

```bash
python3 SKILL_DIR/scripts/publish_run.py <run> --repo TerrenoLabs/terreno-bootstrap-runs
```

It pushes the generated app, with its per-stage commits, to the branch
`runs/<run id>` and points `v<major>.<minor>` at it (so the app's own GitHub
Actions run there), copies `<run>/eval/` to
`results/<major>.<minor>/<run id>/` on `master`, and rebuilds
`results/index.json` and `results/README.md`. It refuses to publish an app
that contains a `.env` file or a value matching a secret pattern.

If the app push is refused (a token without the `workflow` scope cannot push
`.github/workflows/`), publish the scores with `--results-only` and rerun
without it once the token is fixed. Never strip the workflows to get the push
through: CI on the uploaded commit is what the `tests-ci` score depends on.

Then wait for the app branch's CI, and record each workflow's conclusion in
the published `ci.json` (`publish_run.py ci <run> --repo ...`). CI green on
the uploaded commit is part of the `tests-ci` score; update that score file
if the result contradicts the local claim.

### 5. Compare

```bash
python3 SKILL_DIR/scripts/publish_run.py compare --repo TerrenoLabs/terreno-bootstrap-runs
```

Prints, for the newest run of each version against the previous version: the
per-stage score change, the per-stage time change, and any stage that went
from pass to fail. A pass that became fail, a drop of 10 points, or a time
increase of 50% on a stage is a regression. A stage `blocked` on either side
is listed without flags, never as a regression; open the `terreno-skills` PR and the issue drafts
with that table at the top.

### 6. Iterate

When the run ends with skill fixes on a branch:

1. Run the repository's own checks (`bundles.py`, `validate.py`) and open one
   PR with the before and after scores per stage.
2. Rerun the eval for the stages that were fixed, on a fresh app built up to
   the stage before them by replaying the published app branch at that
   stage's commit.
3. Repeat until every stage is at its pass mark, the run's fix budget is
   spent, or the remaining gaps are all docs, framework, or credentials.

Run as a standing loop (for example with a `/loop` or a scheduled agent),
each tick does one thing: if a new minor or major has no published run, start
one; else if the newest run has unfixed skill gaps and budget left, do one fix
round; else do nothing and say nothing.

## Report

End every invocation with this, and nothing longer:

- Version, run id, link to the results folder and the app branch.
- Overall score out of 100 and total time, each with the change from the
  previous version.
- A table: stage, status, score, minutes, attempts.
- Regressions, then blocked stages with what unblocks them.
- Skill fixes made (PR link) and issue drafts written.

## Rules

- Never show a builder the rubric, a score, or a scorer's notes, in any round.
- Never edit the generated app as conductor. A fix that is not in the skill or
  the docs will not be there for the next user.
- Never publish credentials. The publish script's refusal is a stop, not an
  obstacle.
- A number without its evidence file is not a result. Every score cites what
  the scorer ran.
