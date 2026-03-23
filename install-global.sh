#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
FACTORY_HOME="${HOME}/.factory"
PLUGIN_ID="factory-autoresearch-plugin@factory-autoresearch-plugin"

droid plugin marketplace add "$ROOT" || true
droid plugin install "$PLUGIN_ID" --scope user || droid plugin update "$PLUGIN_ID" --scope user

python3 - <<'PY'
import json
from pathlib import Path

settings_path = Path.home() / '.factory' / 'settings.json'
settings = {}
if settings_path.exists():
    settings = json.loads(settings_path.read_text())
settings['todoDisplayMode'] = 'pinned'
settings_path.write_text(json.dumps(settings, indent=2) + '\n')
PY

echo "Installed ${PLUGIN_ID} and set todoDisplayMode=pinned in ${FACTORY_HOME}/settings.json"
