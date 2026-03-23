---
description: Launch the manual autoresearch orchestrator for this repo
argument-hint: <goal / config>
---

Activate the project skill `autoresearch` and treat `$ARGUMENTS` as the user's run goal or config.

Rules:

1. Use the installed Factory skill `autoresearch`.
2. Use the local droids `research-explorer`, `research-critic-a`, `research-critic-b`, `research-judge`, and `research-implementer`.
3. If `$ARGUMENTS` is empty or incomplete, ask only for the missing inputs needed to start safely.
4. Keep autoresearch manual-only. Do not auto-activate it outside explicit `/autoresearch-run` usage unless the user clearly asks in plain language.
5. Before starting experiments, restate the goal, scope, metric, evaluation mode, and guard checks.
6. During the run, maintain one pinned TodoWrite status line and keep `.factory/autoresearch/runs/<run>/status.json` updated.
7. After each completed experiment, recompute improvement and confidence using the skill references.
8. Initialize new runs with the installed autoresearch helper scripts `scripts/init_run.py` and `scripts/update_status.py` from the skill bundle.

If `$ARGUMENTS` includes configuration, parse it and continue.
