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

## When gains stall

If the current line of attack stops producing gains:

1. think outside the box instead of repeating tiny variants
2. question current assumptions and search for a different angle
3. use `WebSearch` or `FetchUrl` when outside research could unblock the run
4. treat external ideas as hypotheses and validate them mechanically before promotion

## Implementation ownership

All experiment changes in the target repo should be made through `research-implementer`, except for autoresearch-owned run artifacts.

The orchestrator may write `run.md`, `results.jsonl`, `status.json`, `lessons.md`, and `summary.md`, but experiment code changes belong to the implementer.
