# Grilling — interactive design interview

Use this during Grow instead of dumping every unknown in one list.

Goal: shared understanding with the user, then write. Do not write the IP, task list, or
code until the user confirms the last round left no open questions. A question the user
explicitly deferred is not open: it is settled as "build on the recommendation" and lands
in the IP's Open questions table (see [Deferral](#deferral)).

Adapted from [grilling](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md).
Do not copy tracker setup from that skill. Follow the consuming repository's artifact and
tracking conventions.

## Map a design tree, not a questionnaire

Every request has a tree:

- **Root:** the destination (what exists when this is done)
- **Branches:** decisions that change the design
- **Leaves:** facts (how the repo already works)

Work in **rounds**. Each round asks only the current **frontier**: questions whose
prerequisites are already settled. Deeper questions wait until their parent is decided.

Example: do not ask "which tracker project?" before "do we track this externally?".
Do not ask "which test double?" before "which public seam is the tracer bullet?".

## Agent vs user

| Kind | Who | How |
| ---- | --- | ---- |
| **Fact** | Agent | Look it up. Spawn explore/generalPurpose sub-agents. Read the repo. |
| **Decision** | User | Ask. Never invent product, scope, or UX choices. |

Do not ask the user anything a sub-agent can answer from the repo, docs, or git history.
If a lookup fails, say what you searched and ask one targeted question.

## Triage every open question

Classify every unknown before the first round. The class decides how it is handled.

| Kind | Test | Handling |
| --- | --- | --- |
| **Fact** | The repo, docs, git history, or a quick probe can answer it | Look it up. Never ask. |
| **Implementation detail** | Repository convention strongly implies the answer | Choose it. List it under Assumptions in the IP. |
| **Deferrable decision** | A human decision, but a wrong guess costs a few tasks' rework | Grill it with a deferral option (see [Deferral](#deferral)). |
| **Fundamental decision** | See below | Grill it to the bottom. Writing blocks until it is settled. |
| **Expansion** | Scope beyond the request: adjacent features, cleanups, "while we're here" ideas | Park it in Expansions. Never put it in the task list. Do not grill it. |

A decision is **fundamental** when at least one holds:

- A wrong guess changes the destination: who it is for, or what exists when it is done.
- A wrong guess rewrites more than half of the task list, usually because it moves the
  tracer seam, data model, or public contract every later task builds on.
- A wrong guess is irreversible or unsafe to discover later: destructive migrations,
  data deletion, PHI exposure, auth or access-control boundaries, external commitments.
- Two options are close and lead to opposite designs, and research cannot break the tie.
- It is a design question whose look is the point of the request.

Anything else is deferrable. When unsure, ask "if I build on my recommendation and the
human picks the other option later, what do I redo?" A few tasks is deferrable. The plan
is fundamental.

Ask fundamental questions in the earliest rounds their prerequisites allow, before
deferrable ones on the same frontier.

## Deferral

Grilling never acts on a recommendation the user has not accepted. Deferral is how the user
accepts one without deciding it now:

- Every **deferrable** question in a round carries one extra option,
  `Use the recommendation (list as open)`, after the real choices. Picking it is consent:
  the plan builds on the recommendation, and the question goes to the IP's
  `## Open questions (recommendation assumed)` table with "If answered differently" and
  "Tasks affected" filled in.
- A **fundamental** question never offers deferral. A reply that tries to defer it stays on
  the frontier with one line on why it cannot wait.
- The user may also defer in words ("go with your recommendations for the rest"). That
  defers every deferrable question still on the frontier, never a fundamental one. Say
  which questions it covered.
- A deferred question is settled for grilling: it unlocks its children on the
  recommended branch.
- A question the user answered goes to Decisions, never to Open questions.

Open questions stay answerable after approval: answering one later moves it to Decisions
and rewrites the tasks its row names.

## Get to the bottom

A reply is not done until Pick can execute it without guessing.

After each user message:

1. Record what was actually chosen, not the wording of the reply.
2. If the answer is vague, partial, "sure", "yes", "whatever you think", or only restates
   the question, stay on that decision. Ask the missing concrete: who, which API, which
   UX, which data owner, which compatibility promise, what is out of scope.
3. If two answers conflict, name the conflict and re-ask the parent before unlocking
   children.
4. If a recommendation had sub-choices and they accepted it without picking one, grill
   the sub-choices.
5. Unlock children only when the parent is executable.

Do not treat a recommended answer as accepted unless the user confirmed it. Do not write
from inferred agreement.

## Round loop

1. Research in parallel (sub-agents). Update the tree.
2. Compute the frontier (undecided questions whose parents are settled).
3. If the frontier is empty, state shared understanding in one short block and wait for
   confirmation. Then write.
4. If the frontier is not empty, ask **every frontier question in this round**, in one
   message. Number them. Recommend an answer for each. Then **stop and wait**.

Never ask only the first question when three are unblocked. Never proceed to the next
round from inferred answers. The user may answer a subset; unanswered items stay on the
frontier. Never ask approval in a frontier round; see [Approval comes last](#approval-comes-last).

### Ask with selectable options, not typed replies

Every frontier round must be answerable by clicking, not by typing `Q1: xyz`.

If the harness has a structured question tool that renders selectable choices
(Cursor `AskQuestion`, Claude Code `AskUserQuestion`, or equivalent), use it for the whole
round instead of listing the questions in prose:

- One tool question per frontier decision; send the round in a single call.
- Cap a structured-tool round at **four** questions. Claude Code `AskUserQuestion` rejects
  calls with more than four, so the fifth frontier question waits for the next round
  instead of being appended. Do not split one round across two calls.
- Put the recommended option **first** and suffix its label with `(Recommended)`.
- Give every question 2–4 concrete, mutually exclusive options. Option labels are the
  actual choice ("Better Auth session cookie", "Existing JWT middleware"), never "Yes"/
  "Option A"/"Your call". The harness always offers a free-text escape, so do not add an
  "Other" option yourself.
- Set multi-select only when the decision genuinely accepts several answers at once.
- A deferrable question adds `Use the recommendation (list as open)` as its last option;
  it counts toward the four-option limit.
- A design question's options are designs, each with an ASCII `preview` naming its
  artboard or file (see [`designing`](designing.md#design-questions)).
- Keep the shaping context in the question prompt, one or two sentences, so the option
  labels stay short.
- Do not also repeat the same questions as numbered prose; the tool is the round.

Only when no such tool exists, fall back to the markdown shape below.

### Fallback message shape (no structured question tool)

Lead with one line: what this round is deciding.

Then for each frontier question:

```markdown
❓ **Q1** — **<short title>**: <context in one or two sentences>
Options (if they help): A / B / C
➡️ Recommend: <your answer, with one-line why>
⏭️ Deferrable: reply "defer" to build on the recommendation and list it as open
---
```

Rules for the body:

- One decision per question.
- Recommend a default every time. The user can override in a word.
- Do not ask for facts you already looked up. Cite the finding in the question if it
  informs the decision.
- Mark fundamental questions `(fundamental)` and omit the deferral line on them.
- Cap the round at **five** questions. Park the rest as "later, after these".
- End the message. Do not write files, do not start Pick, do not summarize the whole
  plan yet. If this branch already has a PR with GitHub Deployments, the last visible
  section is Demo (see the PR deployments procedure).

Round caps, one decision per question: **four** with a structured question tool (the
Claude Code `AskUserQuestion` limit), **five** for the markdown fallback. Anything past the
cap stays on the frontier for the next round.

### After the user replies

1. Record answers on the tree.
2. Get to the bottom of each answered item before treating it as settled.
3. Unlock children. Drop questions the answers made irrelevant.
4. Research any new facts those answers created.
5. Next round, or confirm-and-write if the frontier is empty.

## Confirm-and-write

When the frontier is empty, send **only** this, then wait:

```markdown
Shared understanding:
- Destination: <one sentence>
- In: <comma-separated>
- Out: <comma-separated> (Expansions: <tags, or none>)
- Tracer: <collection / route / hook / CLI>
- Deferred: <question IDs built on the recommendation, or none>
- Open risks: <none | one line>

Confirm and I will write the plan. Change any bullet if I have it wrong.
```

When the harness has a structured question tool, send that block and pair it with one
selectable question ("Confirm this understanding?") offering `Write the plan
(Recommended)` and `Change something` so confirmation is a click too.

If a PR on this branch has GitHub Deployments, print those Demo URLs after this block,
then wait. Do not write the IP until they confirm. This confirmation is not approval:
it unlocks writing and the cut. Approval comes after both.

## Approval comes last

The human approves a plan they have seen with their answers in it, and after the cut has
attacked it. So approval is only ever the last question:

1. Every fundamental question is answered and every deferrable one answered or deferred.
2. The IP is written, cut, and fixed, and cut findings that needed a human were grilled.
3. Post the approval brief, then ask one structured question: `Approve (Recommended)`
   against `Change something`. Without a structured question tool, end the brief with
   "Reply **approve**, or say what to change."

Never ask for approval first, in a frontier round, or alongside an open fundamental
question. Silence is not approval.

## Approval brief

After writing, cutting, and fixing the IP, post one **approval brief**. It is a standalone
document: a reviewer who never saw the grilling rounds, the ticket, or the repository
can read it top to bottom and approve or push back without opening another file. Its top
half is the brief that opens the IP (see [`plan format`](plan-format.md#the-brief-top-of-the-ip));
the chat version adds the Decisions, the Open questions, and the cut tally.

Write it in this order. Orientation first, then the proposal, then the plan, then the
decisions that shaped them, then the pointers.

```markdown
# <Change title>

<Orientation paragraph. Three to five sentences covering where the repository is today,
where this change takes it, and why that is worth doing now. Name the user or operator
who feels the difference. No file paths, no task IDs, no lifecycle jargon.>

## Background

<Current state a reviewer needs before the proposal makes sense: how the affected area
works today, the constraint or gap driving the change, and any research finding that
overturned an obvious approach. Cite the code, docs, or history you read. Omit this
whole section when the orientation paragraph already carries the reader.>

## The idea

<The shape of the solution in a short paragraph or a few bullets: the contract, model,
API, or seam that changes, and what is observably different afterwards. State the
alternative you rejected and why in one line when a reviewer would otherwise ask.>

## The plan

| # | Task | Depends on | Lands in | Proves it |
| --- | --- | --- | --- | --- |
| T1 | <task title> | none | <files or seam> | <test, probe, artifact, or UI exercise> |

Tracer: <public seam the first task cuts through>
Order: <frontier task IDs; blocked task IDs and what unblocks them>
E2E: <planned specs and layers, e.g. "2 specs (browser, http)"; or "None — reason">
Regression: <provisional case IDs and destination suite; or "None — reason">
User guide: <guide pages added, updated, or retired; or "None — reason">
Design: <canvas link and the artboards the plan builds; or "None — reason">
Out of scope: <short tags; see Expansions>
Open risks: <none, or one line each>

## Decisions

| ID | Question asked | Answer | What it changes |
| --- | --- | --- | --- |
| Q1 | <the question as it was asked> | <the settled choice, not a paraphrase of the reply> | <the design consequence a reviewer should check> |

## Open questions (recommendation assumed)

| ID | Question | Recommendation | If answered differently |
| --- | --- | --- | --- |
| Q4 | <the deferred question> | <the choice the plan is built on> | <what changes, and which tasks> |

Cut: <rounds> rounds, <n> findings: <edited> fixed, <grilled> grilled, <moved> moved to questions or expansions, <rebutted> rebutted

## Artifacts

- Plan: <path>
- Tasks: <path, or "in the plan">
- Design: <canvas link and snapshot path, when there is one>
- Supporting skills: <names, or none found>
```

Then the approval question (see [Approval comes last](#approval-comes-last)).

Rules for the brief:

- The first paragraph is the whole change in prose. A reviewer who reads only that
  paragraph should know the destination and the reason.
- Background is optional; everything else is required. Drop Background when the change
  is self-explanatory rather than padding it.
- Skip the Open questions table when nothing was deferred, the same way as Decisions.
  When it has more than five rows, show the five whose answers would change the most
  and point to the IP for the rest.
- The idea and the plan come **before** the Decisions table. Decisions justify the plan;
  they are not the pitch.
- The Decisions table has **no row limit**. List every settled human decision with the
  question that prompted it, so the reviewer can see what was asked and what was chosen.
  Skip the table entirely when grilling settled none; do not mention decisions, an empty
  table, or "none".
- Every acceptance criterion in the plan table names how it is proved. "Manual check" is
  not a verification method.
- Do not restate the IP. The brief orients and points; the IP holds the detail.
- If a PR has GitHub Deployments, print those Demo URLs after the brief.

## Anti-patterns

- One giant question dump at the start
- Prose-only rounds that force typed replies like `Q1: xyz` when the harness can render
  selectable options
- Selectable options that are not real choices ("Yes"/"No"/"Your call") or that duplicate
  the harness's built-in free-text escape
- Asking repository facts ("where is this route defined?")
- Acting on a recommended answer the user has not accepted
- Accepting a vague "yes" as a finished decision
- Recapping the entire interview at the end of every round
- Writing the IP in the same turn as unanswered questions
- Offering deferral on a fundamental question, or treating an unanswered question as
  deferred
- Grilling an expansion instead of parking it
- Asking for approval before the questions it depends on are answered, or before the cut
- A deferred question with no recommendation, or without "If answered differently"
- Hiding decisions in a one-line `Q#=choice` summary
- An approval brief that opens with file paths or task IDs instead of the destination
- A Decisions table that lists choices without the questions that prompted them
- A brief a reviewer cannot act on without opening the IP
