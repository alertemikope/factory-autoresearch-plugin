# Logging Protocol

## Purpose

Logs must let a fresh agent resume the run without hidden memory.

## Minimum files

- `run.md`
- `results.jsonl`
- `status.json`
- `lessons.md`
- `summary.md`

## Result record

Each `results.jsonl` line should contain:

- `iteration`
- `timestamp`
- `mode`
- `metric_name`
- `hypothesis`
- `variant`
- `metric`
- `direction`
- `baseline_metric`
- `best_metric`
- `delta`
- `improvement_pct`
- `confidence_score`
- `confidence_band`
- `status`
- `guard_status`
- `decision`
- `reason`
- `files_touched`

## Status snapshot

`status.json` should contain the latest dashboard state:

- `run_slug`
- `metric_name`
- `direction`
- `runs_completed`
- `baseline_metric`
- `current_metric`
- `best_metric`
- `best_iteration`
- `improvement_pct`
- `confidence_score`
- `confidence_band`
- `last_decision`
- `last_updated_at`

## Lesson format

Capture only durable takeaways:

- what worked
- what failed
- why it likely happened
- when to try or avoid it again

Summarize repeated dead ends instead of duplicating them.
