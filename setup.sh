#!/usr/bin/env sh
# Cognis guided setup wizard — bootstrap one-liner (stdlib Python only).
#
#   ./setup.sh            launch the wizard, then type a number
#   ./setup.sh --dry-run  safe preview: shows commands, runs nothing
#
# Finds python3/python and runs the canonical wizard next to this script.
# With no local MANIFEST.json the wizard auto-fetches the cognis-arsenal
# catalog; override with --manifest <path-or-url> or COGNIS_MANIFEST_URL.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
if command -v python3 >/dev/null 2>&1; then PY=python3
elif command -v python >/dev/null 2>&1; then PY=python
else echo "Python 3 is required (python3 not found on PATH)."; exit 1; fi
exec "$PY" "$DIR/cognis_setup.py" "$@"
