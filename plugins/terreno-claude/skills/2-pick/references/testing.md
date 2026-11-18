# Behavior-first tests

Tests are executable specifications at public seams. A refactor may replace the implementation without changing the test.

## Choose the seam

Before each slice, record the public seam in the task/working notes:

- HTTP route for backend behavior
- exported class/function for package behavior
- rendered component interaction for UI behavior
- injected adapter contract for external systems

Prefer the highest existing seam that proves the behavior. Add a seam only when the production design needs one.

## Red flags

- asserting private methods, internal call order, or call counts
- querying storage directly when the public interface can retrieve the result
- recomputing the expected value with the same algorithm as production
- writing tests for later tasks, or for behavior the task's criteria do not ask for
- deriving tests from the implementation instead of the task's test brief
- testing a mock's behavior instead of the product behavior

Expected values come from a literal worked example, the IP, or another independent source of truth.

## Tests first, per task

Every test for a task is written before that task's implementation, from its test brief
(Seam, Interface, Cases, Blast radius, Test skills; Grow writes it), then confirmed red:
each fails for the reason its case describes. The implementation then works against the
whole set. Tests are written one task at a time, never for the whole IP up front, because
later tasks build on seams earlier ones create.

The writer reads only what a caller sees: exports, signatures, route registrations,
schemas, types, and the helpers and fixtures existing tests near the seam already use.
When the seam does not exist yet, the brief's `Interface` line is the contract; import it
as written there, and the missing module is part of red. Every `Cases` entry and criterion
gets a test with the brief's literal expected values. Add edge cases the criteria imply but
the brief left out, and say which ones were added. A criterion no test at the task's seam
can express is a defect in the brief: report it rather than guess.

## Blast radius

A task that changes state can break behavior it never touches. The brief's `Blast radius`
names each consumer that reads the changed state and the layer its case belongs to. A
backend consumer gets a case in that consumer's existing suite. A user-observable consumer
gets an e2e spec. In an e2e spec, arrange state through the API and act through the UI, and
separate the world the spec only reads (seeded once) from the subject it mutates (created
and reconciled every attempt), so the spec is retry-safe and independent of other specs.

## Repository composition

Load applicable repository testing skills before choosing commands, harnesses, fixtures,
databases, assertion libraries, or runtime probes. In Terreno apps those are
`terreno-backend-tests`, `terreno-frontend-tests`, and `terreno-mobile-tests`; run
`terreno-test-setup` first when the layer has no test setup. Match established tests near the
changed public seam. The lifecycle plugin does not prescribe a framework or package
layout.
