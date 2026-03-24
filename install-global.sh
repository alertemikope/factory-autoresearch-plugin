#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
FACTORY_HOME="${HOME}/.factory"
PLUGIN_ID="factory-autoresearch-plugin@factory-autoresearch-plugin"

DEFAULT_EXPLORER_MODEL="custom:claude-sonnet-4-6"
DEFAULT_CRITIC_A_MODEL="custom:gpt-5.4(high)"
DEFAULT_CRITIC_B_MODEL="custom:claude-opus-4-6(thinking:32000)"
DEFAULT_JUDGE_MODEL="custom:gpt-5.4(xhigh)"
DEFAULT_IMPLEMENTER_MODEL="custom:gpt-5.3-codex-spark"

prompt_model() {
  local label="$1"
  local default_value="$2"
  local env_name="$3"
  local provided="${!env_name:-}"
  local answer=""

  if [ -n "$provided" ]; then
    printf '%s' "$provided"
    return
  fi

  if [ -t 0 ] && [ "${AUTORESEARCH_SKIP_PROMPTS:-0}" != "1" ]; then
    read -r -p "$label [$default_value]: " answer
  fi

  printf '%s' "${answer:-$default_value}"
}

EXPLORER_MODEL="$(prompt_model "Model for research-explorer" "$DEFAULT_EXPLORER_MODEL" AUTORESEARCH_MODEL_EXPLORER)"
CRITIC_A_MODEL="$(prompt_model "Model for research-critic-a" "$DEFAULT_CRITIC_A_MODEL" AUTORESEARCH_MODEL_CRITIC_A)"
CRITIC_B_MODEL="$(prompt_model "Model for research-critic-b" "$DEFAULT_CRITIC_B_MODEL" AUTORESEARCH_MODEL_CRITIC_B)"
JUDGE_MODEL="$(prompt_model "Model for research-judge" "$DEFAULT_JUDGE_MODEL" AUTORESEARCH_MODEL_JUDGE)"
IMPLEMENTER_MODEL="$(prompt_model "Model for research-implementer" "$DEFAULT_IMPLEMENTER_MODEL" AUTORESEARCH_MODEL_IMPLEMENTER)"

droid plugin marketplace add "$ROOT" || true
droid plugin install "$PLUGIN_ID" --scope user || droid plugin update "$PLUGIN_ID" --scope user

python3 - "$EXPLORER_MODEL" "$CRITIC_A_MODEL" "$CRITIC_B_MODEL" "$JUDGE_MODEL" "$IMPLEMENTER_MODEL" <<'PY'
import json
import re
import sys
from pathlib import Path

settings_path = Path.home() / '.factory' / 'settings.json'
settings = {}
if settings_path.exists():
    settings = json.loads(settings_path.read_text())
settings['todoDisplayMode'] = 'pinned'
settings_path.write_text(json.dumps(settings, indent=2) + '\n')

model_map = {
    'research-explorer.md': sys.argv[1],
    'research-critic-a.md': sys.argv[2],
    'research-critic-b.md': sys.argv[3],
    'research-judge.md': sys.argv[4],
    'research-implementer.md': sys.argv[5],
}

cache_root = Path.home() / '.factory' / 'plugins' / 'cache' / 'factory-autoresearch-plugin' / 'factory-autoresearch-plugin'
for droids_dir in cache_root.glob('*/droids'):
    for filename, model in model_map.items():
        path = droids_dir / filename
        if not path.exists():
            continue
        text = path.read_text()
        updated = re.sub(r'^model:\s*.*$', f'model: "{model}"', text, flags=re.M)
        path.write_text(updated)

print(json.dumps({'todoDisplayMode': 'pinned', 'models': model_map}, indent=2))
PY

echo "Installed ${PLUGIN_ID} and set todoDisplayMode=pinned in ${FACTORY_HOME}/settings.json"
