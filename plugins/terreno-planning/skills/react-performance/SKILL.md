---
name: react-performance
description: >-
  Investigate and fix React render performance for one component or one page by measuring
  it: count every component render as props change or a user interacts (bippy, the engine
  behind react-scan), classify each render's cause, fix the wasted ones, re-measure, and
  lock the result in with a render-budget test. Works for React, React Native, and React
  Native Web. Use when asked to profile or speed up a component or screen, reduce or
  explain re-renders, find out why something re-renders, check that memoization works, or
  fix a laggy list, form, or typing lag. Not for bundle size, network or query latency,
  slow backend calls, or startup time.
---

# React render performance

Measure which components render, how often, and why; fix the renders that could not have
changed the output; prove the fix with the same measurement.

Done when all of these hold:

- A before and an after audit of the same scenario exist, and `compareAudits.ts` exits 0.
- Every wasted render left in the after audit has a one-line reason it stays.
- A render-budget test fails on the old code and passes on the new code.
- The component's existing tests pass, and the UI was exercised once in the running app.

Never change code on a guess. No fix without a before number; no claim without an after
number.

## What the audit reports

Each **step** is one prop change or interaction. For every component that rendered in the
step, the audit gives mounts, updates, and the cause of each update:

| Cause | Meaning | Wasted? |
| --- | --- | --- |
| `mount` | first render | no |
| `props` | a prop changed value | no |
| `state` | its own state or reducer changed | no |
| `context` | a context it reads changed | no |
| `unstable-props` | every prop is equal by value, but one or more has a new identity | yes |
| `parent` | nothing it reads changed; its parent rendered | yes |

**Fix here** counts wasted renders whose parent component did not itself waste a render.
That is the top of a wasted subtree: fix those rows first and the rows under them
disappear. **Unstable props** names the props to stabilize.

## Setup, once per package

The scripts import `bippy`, so they must live inside the package under test. `$SKILL` is
this skill's directory.

1. Add the dependency to the package that owns the component, pinned:
   `bun add -d bippy@0.7.3`.
2. Copy `$SKILL/scripts/*.ts` into the package's test-helper or benchmark folder (in
   Terreno's `ui/`: `benchmarks/renderAudit/`). Do not edit `renderAudit.ts`; fix it in
   this skill instead.
3. Run audits with `preload.ts` as the **first** preload, before the package's own setup:

   ```bash
   bun test --preload ./benchmarks/renderAudit/preload.ts --preload ./src/bunSetup.ts \
     ./benchmarks/renderAudit/
   ```

   React only reports to a devtools hook that exists before the renderer loads. If the
   audit throws `no commits seen`, the preload is missing or not first.

## Component workflow

1. **Write the scenario** as a test file next to the scripts. Render through the package's
   normal test wrapper and drive `auditPropChanges`:

   ```tsx
   import {auditPropChanges, createRenderAudit, formatReport} from "./renderAudit";

   const audit = createRenderAudit({ignore: /^(ThemeProvider|TerrenoFontProvider)$/});
   let view: ReturnType<typeof renderWithTheme> | undefined;
   await auditPropChanges({
     audit,
     baseline,
     changes: {
       "new onChange identity": {...baseline, onChange: (): void => {}},
       "one option selected": {...baseline, value: ["a", "b"]},
     },
     mount: (props) => { view = renderWithTheme(<Component {...props} />); },
     update: (props) => { view?.rerender(<Component {...props} />); },
   });
   console.info(formatReport(audit.report()));
   ```

   It runs `mount`, then `same props` (the parent re-rendered and nothing changed), then
   one step per entry in `changes`, resetting to `baseline` between steps so each step
   measures one change. Always include these changes:

   - each prop a user changes in normal use (value, selection, page, text), one at a time;
   - **a new identity for each callback prop**, because callers pass inline handlers;
   - **a new array or object with equal contents** for each collection prop;
   - for lists, at least 8 items, so per-row waste is visible.

   `ignore` the wrapper components your own `rerender` call re-renders; they are harness
   noise. For interactions instead of props, use `audit.step("label", () => fireEvent…)`.

2. **Record the baseline** before touching the component: write `audit.report()` as JSON
   to `before/<Name>.json` and keep the printed tables.

3. **Read the report top down.** Rows are sorted by Fix here. For each row with Fix here
   above zero, pick the fix from the table below. Ignore wasted `View`, `Text`, and
   `Pressable` rows that sit under a wasted row of your own component.

   | Report shows | Fix |
   | --- | --- |
   | Row component: `unstable-props`, a callback prop named | Parent passes a stable handler (`useCallback`, or a stable wrapper that calls the latest handler) and the row calls it with its own id; wrap the row in `memo` |
   | Row component: `unstable-props`, an object, array, or `style` prop named | Hoist the constant to module scope, or `useMemo` it; pass primitives instead of an object when only two or three fields are used |
   | Child: `parent`, and its props are already stable | Wrap the child in `memo` |
   | List rows all update when one row's data changes | Extract the row into its own `memo` component with primitive props and a stable key |
   | Whole component: `parent` in `same props` | `memo` the component only when it renders many nodes or sits in a list; a cheap leaf is not worth it |
   | `state` updates on every keystroke or tick in a large component | Move that state into the smallest child that needs it |
   | `context` on many components after an unrelated change | Memoize the provider value; split the context so fast-changing values are separate |
   | Default prop like `onChange = () => {}` or `items = []` listed as unstable | Replace it with a module-level constant |

4. **Fix one cause at a time**, then re-run. Keep a fix only if the numbers moved.

5. **Compare.** Write the after report to `after/<Name>.json`, then:

   ```bash
   bun $SKILL/scripts/compareAudits.ts before/<Name>.json after/<Name>.json
   ```

   It prints renders and wasted renders per step and exits 1 when a step wastes more than
   before or total renders rise. A `mount` step may gain a few renders when you extract a
   row component; that is fine if the total falls.

6. **Lock it in.** Turn the scenario into an assertion on the step that matters:

   ```tsx
   expect(componentStat(report, "one option selected", "Option")?.updates).toBe(1);
   expect(componentStat(report, "new onChange identity", "Option")).toBeUndefined();
   ```

   Assert counts of your own components, not totals, so a library upgrade does not break
   the test. Confirm it fails with the fix stashed.

7. **Verify behavior.** Run the component's existing tests. Then exercise the component in
   the running app (in Terreno, `verify-ui-changes`): memoization bugs show up as stale
   UI, which render counts cannot see.

## Page workflow

For a screen in a running web app, the same collector runs in the browser through
Playwright. Use a development build or an unminified export
(`expo export -p web --no-minify`): minified bundles rename every component.

```ts
import {chromium} from "playwright";
import {attachRenderAudit} from "./pageAudit";
import {formatReport} from "./renderAudit";

const browser = await chromium.launch();
const page = await browser.newPage();
const audit = await attachRenderAudit({page});          // before page.goto
await page.goto("http://localhost:8082/todos");
await page.getByTestId("todos-screen").waitFor({state: "visible"});
await audit.endLoad();                                  // closes the "load" step
await audit.step("type in search", async () => {
  await page.getByTestId("todos-search-input").pressSequentially("milk");
});
console.info(formatReport(await audit.report(), {limit: 15}));
await browser.close();
```

- One step per user action: typing, toggling, opening a modal, paging, scrolling a list.
- A page renders hundreds of components. Pass `only: /^(TodoRow|TodoList|…)$/` once you
  know which ones matter, or read only the Fix here rows.
- Wait for the UI to settle inside the step (a `waitFor` on the result), or late commits
  land outside it.
- Once a page step points at a component, switch to the component workflow for the fix
  and the budget test; page audits are for finding, not for locking in.
- Native-only screens: audit the component under the test renderer instead.

## Judgment rules

- **A render count is evidence, not a defect.** One wasted render of a cheap leaf does not
  matter. Fix waste that multiplies: list rows, table cells, every keystroke, every tick.
- **Functions with identical source count as equal.** A handler that closes over a changed
  value still shows as `unstable-props`. Read the handler before removing its re-render.
- **`memo` needs stable props to work.** Adding `memo` to a child whose parent passes an
  inline callback changes nothing; the audit will show the same count. Fix the prop first.
- **Do not hand-memoize under React Compiler.** If the project enables it, components
  already memoize; report remaining waste instead of adding `useMemo`.
- **Never trade correctness for a count.** Do not drop a dependency from a hook, compare
  props with a custom `memo` comparator that skips fields, or read stale state.
- **Test-renderer counts are not frame times.** They prove fewer renders, not a faster
  frame. For a user-visible claim, also record the page workflow or a device profile.

## Report

```markdown
## Scenario
<component or URL>, steps audited

## Results
<compareAudits table per component>

## Fixes
1. `path/file.tsx:line`: cause from the audit → change made → renders before → after

## Left as is
- `<Component>` in `<step>`: N wasted, reason it stays

## Locked in by
`path/Component.audit.test.tsx` (fails on the old code)
```
