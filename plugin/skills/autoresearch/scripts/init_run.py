#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or "run"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_run_markdown(args, run_slug: str, created_at: str) -> str:
    lines = [
        f"# Autoresearch Run: {run_slug}",
        "",
        f"- Created: {created_at}",
        f"- Goal: {args.goal}",
        f"- Scope: {args.scope or 'TBD'}",
        f"- Evaluation mode: {args.mode}",
        f"- Metric: {args.metric_name}",
        f"- Direction: {args.direction}",
        f"- Verify: {args.verify or 'TBD'}",
        f"- Guard: {args.guard or 'none'}",
        "",
        "## Notes",
        "",
        "- Baseline established before the first non-baseline experiment.",
        "- Update `summary.md`, `results.jsonl`, and `status.json` after each completed experiment.",
    ]
    return "\n".join(lines) + "\n"


def build_summary_markdown(args, baseline_metric) -> str:
    return (
        "# Summary\n\n"
        f"- Goal: {args.goal}\n"
        f"- Metric: {args.metric_name}\n"
        f"- Baseline: {baseline_metric if baseline_metric is not None else 'pending'}\n"
        "- Best run: baseline\n"
        "- Strongest lesson: pending\n"
        "- Next step: start the first judged experiment\n"
    )


def build_lessons_markdown() -> str:
    return (
        "# Lessons\n\n"
        "## Wins\n\n"
        "- None yet.\n\n"
        "## Dead ends\n\n"
        "- None yet.\n"
    )


def build_status(run_slug: str, args, created_at: str, baseline_metric):
    return {
        "run_slug": run_slug,
        "metric_name": args.metric_name,
        "direction": args.direction,
        "runs_completed": 0,
        "baseline_metric": baseline_metric,
        "current_metric": baseline_metric,
        "best_metric": baseline_metric,
        "best_iteration": 0 if baseline_metric is not None else None,
        "improvement_pct": 0.0 if baseline_metric is not None else None,
        "confidence_score": None,
        "confidence_band": "n/a",
        "last_decision": "baseline" if baseline_metric is not None else "initialized",
        "last_updated_at": created_at,
    }


def append_baseline(results_path: Path, args, created_at: str, baseline_metric):
    if baseline_metric is None:
        results_path.write_text("")
        return
    record = {
        "iteration": 0,
        "timestamp": created_at,
        "mode": args.mode,
        "metric_name": args.metric_name,
        "hypothesis": "baseline",
        "variant": "baseline",
        "metric": baseline_metric,
        "direction": args.direction,
        "baseline_metric": baseline_metric,
        "best_metric": baseline_metric,
        "delta": 0.0,
        "improvement_pct": 0.0,
        "confidence_score": None,
        "confidence_band": "n/a",
        "status": "baseline",
        "guard_status": "n/a" if not args.guard else "pending",
        "decision": "baseline",
        "reason": "initial baseline",
        "files_touched": [],
    }
    results_path.write_text(json.dumps(record) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Initialize autoresearch run artifacts")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--metric-name", required=True)
    parser.add_argument("--direction", choices=["higher", "lower"], required=True)
    parser.add_argument("--mode", choices=["direct", "harness"], required=True)
    parser.add_argument("--slug")
    parser.add_argument("--scope")
    parser.add_argument("--verify")
    parser.add_argument("--guard")
    parser.add_argument("--baseline-metric", type=float)
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    run_root = repo / ".factory" / "autoresearch" / "runs"
    run_root.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_slug = f"{timestamp}-{slugify(args.slug or args.goal[:48])}"
    run_dir = run_root / run_slug
    run_dir.mkdir(parents=True, exist_ok=False)

    created_at = now_iso()

    (run_dir / "run.md").write_text(build_run_markdown(args, run_slug, created_at))
    (run_dir / "summary.md").write_text(build_summary_markdown(args, args.baseline_metric))
    (run_dir / "lessons.md").write_text(build_lessons_markdown())
    append_baseline(run_dir / "results.jsonl", args, created_at, args.baseline_metric)
    (run_dir / "status.json").write_text(json.dumps(build_status(run_slug, args, created_at, args.baseline_metric), indent=2) + "\n")

    print(json.dumps({"run_dir": str(run_dir), "run_slug": run_slug}, indent=2))


if __name__ == "__main__":
    main()
