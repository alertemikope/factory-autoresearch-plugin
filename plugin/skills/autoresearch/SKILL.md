---
name: autoresearch
description: Orchestrate Droid autoresearch runs with persistent logs, structured debate between specialized droids, direct-metric or harness evaluation, and optional parallel hypothesis testing.
disable-model-invocation: true
---

# Autoresearch

Use this skill when the user wants Droid to run or design an autonomous improve-verify-decide loop.

## Role

This skill is the orchestrator. It does not act like a single researcher.

- Use `research-explorer` to generate bold but testable ideas.
- Use `research-critic-a` to produce the first adversarial review.
- Use `research-critic-b` to challenge both the proposals and critic A's reasoning.
- Use `research-judge` to resolve disagreements, select the next experiment, decide whether to parallelize, and enforce stop criteria.
- Use `research-implementer` to translate the judge's selected experiment into concrete edits.

## Required inputs

Collect or infer these before starting:

- Goal
- Editable scope
- Evaluation mode: `direct` or `harness`
- Primary metric
- Direction: `higher` or `lower`
- Verify command or evaluator
- Optional guard checks
- Optional holdout set
- Optional budget and iteration cap

If any critical field is missing, ask for it before launching the loop.

## Startup protocol

1. Read `references/loop.md`, `references/debate.md`, `references/evaluation.md`, `references/logging.md`, and `references/parallel.md`.
2. Inspect the repo and define the smallest safe editable scope.
3. Choose the evaluation mode:
   - `direct`: benchmark, tests, typecheck, build, latency, coverage, error count.
   - `harness`: prompt, skill, workflow, or agent behavior scored by a repeatable evaluator.
4. Establish a baseline before any experiment.
5. Initialize the run with `scripts/init_run.py` so `run.md`, `results.jsonl`, `status.json`, `lessons.md`, and `summary.md` are created in a consistent format.
6. Maintain the live dashboard state with `scripts/update_status.py` after each completed experiment.
7. Initialize a single pinned TodoWrite line for the live run summary.

## Monitoring

Factory project config cannot add a fully custom native widget above the chat input, so use the closest supported pattern:

- keep `todoDisplayMode` pinned for this project
- maintain one live TodoWrite item during the run
- persist the same snapshot to `status.json`
- expose a richer table view through `/autoresearch-status`

Update the pinned status after the baseline and after every completed experiment.

Use this format for the live summary line:

`Autoresearch: <runs> runs | best <metric_name>: <best_value> (<improvement_pct>) | conf <confidence_label> | last <decision>`

If confidence is unavailable, show `conf n/a`.

## Debate-first loop

For each iteration:

1. Read the latest baseline, recent results, and lessons.
2. Ask `research-explorer` for 2-3 concrete hypotheses.
3. Ask `research-critic-a` to challenge those hypotheses and identify the strongest objections.
4. Ask `research-critic-b` to challenge the same hypotheses, critique critic A when relevant, and surface the key disagreement.
5. Ask `research-judge` to select:
   - one experiment for serial execution, or
   - up to two experiments for isolated parallel execution.
6. Ask `research-implementer` to implement the selected experiment, or each isolated variant if parallel mode was approved.
7. Run the selected experiment.
8. Evaluate mechanically.
9. Decide: `keep`, `discard`, `retry`, `pivot`, or `stop`.
10. Write the result row to `results.jsonl`.
11. Run `scripts/update_status.py` for the current run directory, then update the pinned TodoWrite line from the resulting `status.json`.
12. Write a short lesson.

Never treat debate as proof. Only measured results can promote a change.

## Decision policy

- Keep only changes that improve the target metric and satisfy guards.
- Discard changes that regress the metric, fail guards, or reward-hack the evaluator.
- Retry only when noise or nondeterminism is the likely cause.
- Pivot after repeated discards on the same strategy.
- Prefer the simpler change when results are materially equal.

## Parallel mode

Parallel mode is optional.

- Parallelize proposal generation freely.
- Parallelize code experiments only in isolated branches or worktrees.
- Never let two workers edit the same worktree.
- Merge only the winning experiment back into the main line.

## Required artifacts

Each run should maintain:

- `run.md` — goal, scope, metric, constraints, current plan
- `results.jsonl` — one record per iteration
- `status.json` — live monitoring snapshot for widget and dashboard views
- `lessons.md` — validated wins, failures, and anti-patterns
- `summary.md` — current best result, open questions, next actions

When using harness evaluation, also maintain:

- `dataset.jsonl` or equivalent case list
- `holdout.jsonl` if a holdout split exists
- `scorecard.json` for latest aggregate results

## Safety rules

- Do not merge, deploy, publish, or delete broad user data unless the user explicitly asks.
- Do not widen editable scope during the loop without a clear reason.
- Do not keep a change based only on model preference or debate consensus.
- Do not optimize on the same examples used to judge final quality when holdout data exists.

## Completion

At the end of the run, report:

- baseline vs best result
- kept vs discarded experiments
- strongest validated lesson
- next recommended strategy
