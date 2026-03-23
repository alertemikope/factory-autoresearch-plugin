# Parallel Experiments

## When to parallelize

Parallelize only when the bottleneck is idea evaluation, not shared mutable state.

Good candidates:

- comparing prompt variants
- trying independent parameter changes
- testing multiple isolated code strategies in separate worktrees

## Isolation rules

- one worker per branch or worktree
- no shared editable files in the same working tree
- shared baseline and evaluator definition
- merge only the winning result

## Batch size

Default to 2 parallel experiments.

Increase only if:

- the evaluator is cheap
- the repo supports clean isolation
- the user budget allows it

## Winner selection

Use the same judge rubric for serial and parallel runs. The winner must still pass all guards before promotion.
