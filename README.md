# factory-autoresearch-plugin

Factory autoresearch plugin with:

- debate droids (`explorer`, `critic-a`, `critic-b`, `judge`, `implementer`)
- manual slash commands
- pinned live status
- confidence scoring based on MAD
- `status.json` + `results.jsonl` run artifacts

## What it installs

- a Factory marketplace at the repo root
- one installable plugin under `plugin/`
- slash commands:
  - `/autoresearch-run`
  - `/autoresearch-status`
  - `/autoresearch-stop`

## Install

### Option 1: Factory plugin install

```bash
droid plugin marketplace add https://github.com/alertemikope/factory-autoresearch-plugin
droid plugin install factory-autoresearch-plugin@factory-autoresearch-plugin --scope user
```

### Option 2: one-command global install

```bash
git clone https://github.com/alertemikope/factory-autoresearch-plugin.git
cd factory-autoresearch-plugin
./install-global.sh
```

`install-global.sh` also sets:

```json
{
  "todoDisplayMode": "pinned"
}
```

## Required custom model aliases

This plugin is configured to use these custom model names in `~/.factory/settings.json` under `customModels[].model`:

| Role | Required custom model |
| --- | --- |
| `research-explorer` | `claude-sonnet-4-6` |
| `research-critic-a` | `gpt-5.4(high)` |
| `research-critic-b` | `claude-opus-4-6(thinking:32000)` |
| `research-judge` | `gpt-5.4(xhigh)` |
| `research-implementer` | `gpt-5.3-codex-spark` |

If another computer does not have these aliases, either:

1. add the same custom model entries to `~/.factory/settings.json`, or
2. edit the droid files under `plugin/droids/` before installing.

## Usage

### Start a run

```text
/autoresearch-run reduce p95 latency for search endpoint
```

### Check the dashboard

```text
/autoresearch-status
```

### Stop safely

```text
/autoresearch-stop
```

## Monitoring

During a run, the workflow keeps a pinned status line with:

- run count
- best metric
- improvement percentage
- confidence score
- last decision

The detailed dashboard is computed from:

- `run.md`
- `results.jsonl`
- `status.json`
- `lessons.md`
- `summary.md`

under:

```text
.factory/autoresearch/runs/<timestamp>-<slug>/
```

## Confidence scoring

After 3 or more numeric runs, confidence is computed as:

```text
confidence = |best_improvement| / MAD
```

where `MAD` is the median absolute deviation of all metric values in the current run.

Interpretation:

- `>= 2.0x` → likely real
- `1.0x - < 2.0x` → marginal
- `< 1.0x` → within noise

This is advisory only. It should trigger caution or re-runs, not automatic discard.

## Repo structure

```text
.factory-plugin/marketplace.json
plugin/
  .factory-plugin/plugin.json
  commands/
  droids/
  skills/autoresearch/
install-global.sh
README.md
```
