# Run Control

## Helper scripts

Never search the target repository for autoresearch helper scripts.

Use the installed autoresearch helper scripts directly:

- `~/.factory/skills/autoresearch/scripts/init_run.py`
- `~/.factory/skills/autoresearch/scripts/update_status.py`

If those paths do not exist, use the installed skill bundle path, not the target repo.

## Todo / widget behavior

During an active autoresearch run, do not use a multi-step TodoWrite plan.

Use exactly one pinned TodoWrite item in progress:

`1. [in_progress] Autoresearch: <runs> runs | best <metric_name>: <best_value> (<improvement_pct>) | conf <confidence_label> | last <decision>`

Keep implementation planning in run artifacts, not in the visible todo list.

## Progress updates

If the user asks for an update during a run:

1. summarize current state briefly
2. do not ask whether to continue
3. continue automatically unless the user explicitly asks to stop or pause

## Implementation ownership

All experiment changes in the target repo should be made through `research-implementer`, except for autoresearch-owned run artifacts.

The orchestrator may write `run.md`, `results.jsonl`, `status.json`, `lessons.md`, and `summary.md`, but experiment code changes belong to the implementer.
