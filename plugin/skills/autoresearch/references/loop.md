# Loop Protocol

## Core invariant

Autoresearch is a closed loop:

1. observe
2. hypothesize
3. modify
4. evaluate
5. decide
6. log
7. repeat

## Iteration shape

Each iteration should change only one strategy at a time unless the run is explicitly in isolated parallel mode.

## Stop conditions

Stop when one of these is true:

- user target is met
- budget is exhausted
- guard failures make the search unsafe
- the current evaluator is no longer trustworthy
- the repo cannot support more safe experiments

## Pivot triggers

Pivot when:

- 3 consecutive experiments on the same idea family fail
- the critic repeatedly identifies the same confounder
- the judge flags reward hacking or evaluator leakage
- a simpler baseline dominates all recent variants
