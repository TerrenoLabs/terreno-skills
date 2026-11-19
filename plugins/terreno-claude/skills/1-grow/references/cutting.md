# Cutting — attack the IP with the human's eyes

The agent that wrote a plan cannot see its own drift, because its research and reasoning
fill the gaps. The cut gives a fresh attacker only what the human said plus the IP, so
every gap shows. Grow runs it at step 10, after writing and before approval. It can also
run on any existing IP before someone approves it.

The cut never edits the IP. It returns findings, and Grow fixes them.

## Build the user-context packet

Collect, verbatim:

1. The original request: the human's message, ticket, or spec text, plus any linked
   material the human supplied.
2. Every reply the human gave during grilling: the options picked, free-text answers,
   and deferrals.
3. The IP file path.

Leave out Grow's research notes, execution state, transcript, reasoning, and summaries of
what the human "meant". Paraphrase is the thing under attack. When run on an IP with no
transcript, use the ticket or PR the IP cites and the IP's Decisions table as the human's
words, and say so in the report.

## Launch the attacker

Spawn one **fresh** subagent with no inherited context (Claude Code: `general-purpose`,
never a fork, which inherits the planner's context). Pass the packet and this brief:

> You are reviewing an implementation plan on behalf of the person who asked for it. You
> have what they said and the plan. Assume the plan is wrong somewhere and find where.
> You may read the repository files the IP cites, to check a claim it makes about the
> code. Do not read `.terreno/`, planning transcripts, or anything else about how the
> plan was made.
>
> Attack on these axes:
>
> 1. **Fidelity.** Something they asked for that is missing, weakened, or deferred.
>    Something in the task list they did not ask for (belongs in Expansions).
> 2. **Assumed answers.** Open-question recommendations or Assumptions that conflict
>    with what they said, or that they would likely reject. Assumptions stated as facts.
>    A Decision whose Answer does not match what they actually chose.
> 3. **Mis-triage.** An Assumption or Open question that is really a fundamental human
>    decision: a wrong guess would change the destination, rewrite most tasks, or be
>    irreversible or unsafe (data deletion, PHI exposure, auth boundaries).
> 4. **Proof.** Acceptance criteria that are not observable or have no real
>    verification method. A task whose test brief a tester could not write tests from
>    without seeing the implementation: no Interface, Cases without literal expected
>    values, missing error and permission cases, a state-changing task with no Blast
>    radius, or an `untestable` claim a test could disprove.
> 5. **Executability.** A task a fresh engineer could not start without guessing:
>    missing seams, wrong order, hidden dependencies, claims about the code that are false.
> 6. **Risk.** PHI or security exposure, data migration, irreversible operations,
>    rollout and compatibility gaps the plan does not address.
> 7. **Decomposition.** Two tasks that write the same file with no dependency between
>    them; a task that is really two independently roast-able behaviours; a chain that
>    could be a fan-out; a dependency with no real read/extend relationship; a chain
>    longer than three without a reason per link; a `Files:` line that omits a shared
>    registry, index, or barrel the task must edit. Check `Depends on:` against `Files:`
>    and the proof for each task.
> 8. **Readability.** The brief does not make sense to someone who knows only the request.
> 9. **Testing plan and user guide.** Each of these is `blocking`:
>    - the IP has no `## E2E tests` or no `## Regression cases` section;
>    - the IP has no `## User guide` section;
>    - a section says `None` with no reason (`None — <reason>` is fine);
>    - a UI or cross-process acceptance criterion has no planned spec in `## E2E tests`,
>      and the section gives no reason;
>    - a user-visible criterion has no `## User guide` row, and the section gives no
>      reason (a repository whose `## User guide conventions` table says `none` writes
>      `None — user guide off`).
>
>    Also attack regression steps with no concrete starting state, action, or observable
>    Expected, and a regression case an e2e guide layer could fully automate or that
>    repeats an existing suite case (`should-fix`: regression is usually
>    `None — no hard-to-automate change`). Attack guide rows whose page would describe
>    unshipped behavior or use code names instead of on-screen words. An IP whose
>    Sign-off already reads `Status: approved` was approved before these contracts if it
>    lacks a section: read the section as `None — predates contract` and report it as
>    `should-fix`, not `blocking`.
>
>    Attack the `## Design` section the same way, as `should-fix`: a missing section or a
>    bare `None`, a UI task with no `Design:` line when the IP links a canvas, an artboard
>    no task delivers that is not an Expansion, and a canvas that contradicts a criterion
>    or Decision.
>
> Return at most 12 findings, most severe first, as a markdown table:
> `ID | Severity (blocking / should-fix / nit) | Axis | Where in the IP | Attack | Evidence | Suggested fix`.
> Evidence is a quote of their words, a quote of the IP, or a file and line. A finding
> without evidence is dropped. "No findings" is a valid answer; do not invent any.
>
> After the table, add two short sections, one line each, or `None.`:
>
> - **Well-reasoned:** a part of the plan you attacked that held up, with the evidence
>   that it holds.
> - **Couldn't assess:** a part you could not check, and why: no access, no transcript,
>   a claim about an external system or data you cannot see.
>
> An empty table must not read as a clean plan when you could not check it. Do not pad
> either list.

## Return

The attacker's report comes back with one line on top:
`Cut: <n> findings (<b> blocking), <w> well-reasoned, <u> couldn't assess on <IP path>, context: <transcript | ticket+Decisions>`.

Grow resolves each finding per its step 10 and records the tally in `## Sign-off`. When a
human runs the cut on its own, print the table and offer to apply the fixes through Grow;
do not apply them in the cut.
