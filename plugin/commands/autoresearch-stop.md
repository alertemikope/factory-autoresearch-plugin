---
description: Stop the current autoresearch run and summarize the state
---

Stop the current autoresearch run for this repo.

Rules:

1. Do not launch any new autoresearch experiments.
2. If an autoresearch loop is active in the current conversation, stop after the current safe boundary.
3. Summarize the current state:
   - baseline vs best known result
   - last completed experiment
   - kept vs discarded experiments if known
   - latest confidence score and whether the current win is likely real or still noisy
   - strongest lesson so far
   - safest next step if the run resumes later
4. If no autoresearch run is active, say that nothing is currently running.
5. Finalize the pinned TodoWrite status line instead of leaving a stale live widget.
6. Do not delete run artifacts unless the user explicitly asks.
