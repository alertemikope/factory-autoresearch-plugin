# Evaluation Modes

## Direct mode

Use direct mode when the target metric comes from the real system:

- test runtime
- build time
- benchmark latency
- type error count
- lint count
- coverage
- pass rate

Guidelines:

- keep the evaluator as close as possible to production reality
- use guard commands for regression prevention
- rerun noisy benchmarks before deciding

## Harness mode

Use harness mode when optimizing prompts, skills, workflows, or agent behavior.

Required pieces:

- a repeatable case set
- a scoring function or judge protocol
- an optional holdout split
- explicit anti-reward-hacking checks

Recommended minimum:

- score on training cases
- verify on holdout before promoting the change
- log per-case failures, not only aggregate score

## Anti-Goodhart rules

- never optimize only for one synthetic case
- use holdout scenarios when possible
- reject changes that improve score by exploiting format quirks or evaluator leakage
- keep a human-readable explanation for every promoted change

## Confidence scoring

After 3 or more numeric experiment results in the current run, compute a confidence score to distinguish real gains from noise.

### Formula

- `MAD = median(|x - median(all_metric_values)|)`
- `best_improvement = absolute gain of the current best result vs baseline`
- `confidence = |best_improvement| / MAD`

If `MAD` is zero and the best improvement is positive, treat confidence as effectively infinite. If there are fewer than 3 numeric results, confidence is unavailable.

### Interpretation

- `>= 2.0x` — likely real
- `1.0x to < 2.0x` — marginal but above noise
- `< 1.0x` — within noise, re-run before trusting the win

### Policy

- Confidence is advisory only.
- Low confidence should trigger re-runs or caution, not automatic discard.
- Persist confidence on each result row and in `status.json`.
