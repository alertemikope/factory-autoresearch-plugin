#!/usr/bin/env python3
import argparse
import json
import math
import statistics
from datetime import datetime, timezone
from pathlib import Path


def load_rows(path: Path):
    rows = []
    if not path.exists():
        return rows
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def confidence_band(score):
    if score is None:
        return "n/a"
    if math.isinf(score) or score >= 2.0:
        return "likely-real"
    if score >= 1.0:
        return "marginal"
    return "within-noise"


def main():
    parser = argparse.ArgumentParser(description="Recompute autoresearch status.json from results.jsonl")
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    results_path = run_dir / "results.jsonl"
    status_path = run_dir / "status.json"
    rows = load_rows(results_path)
    if not rows:
        raise SystemExit("results.jsonl is empty or missing")

    metric_rows = [(row, row.get("metric")) for row in rows if isinstance(row.get("metric"), (int, float))]
    if not metric_rows:
        raise SystemExit("No numeric metric rows found")

    first_row, baseline = metric_rows[0]
    direction = first_row.get("direction", "lower")
    if direction == "higher":
        best_row, best_metric = max(metric_rows, key=lambda item: item[1])
        best_improvement = best_metric - baseline
    else:
        best_row, best_metric = min(metric_rows, key=lambda item: item[1])
        best_improvement = baseline - best_metric

    current_row, current_metric = metric_rows[-1]
    values = [metric for _, metric in metric_rows]
    confidence_score = None
    if len(values) >= 3:
        median = statistics.median(values)
        mad = statistics.median([abs(value - median) for value in values])
        if mad == 0:
            confidence_score = math.inf if best_improvement > 0 else 0.0
        else:
            confidence_score = abs(best_improvement) / mad

    improvement_pct = None if baseline == 0 else (best_improvement / abs(baseline)) * 100.0
    runs_completed = len([row for row, _ in metric_rows if row.get("status") != "baseline" and row.get("iteration") != 0])

    status = {
        "run_slug": run_dir.name,
        "metric_name": current_row.get("metric_name", "metric"),
        "direction": direction,
        "runs_completed": runs_completed,
        "baseline_metric": baseline,
        "current_metric": current_metric,
        "best_metric": best_metric,
        "best_iteration": best_row.get("iteration"),
        "improvement_pct": improvement_pct,
        "confidence_score": confidence_score,
        "confidence_band": confidence_band(confidence_score),
        "last_decision": current_row.get("decision", current_row.get("status", "n/a")),
        "last_updated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    status_path.write_text(json.dumps(status, indent=2) + "\n")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
