#!/usr/bin/env bash
# Start excalidraw-mcp canvas server (connected mode) for MCP export_scene / live sync.
# Open http://127.0.0.1:3000 after start. API key from .env (see .env.example).

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=scripts/load_excalidraw_env.sh
source "$ROOT/scripts/load_excalidraw_env.sh"
load_excalidraw_env "$ROOT"

export CANVAS_HOST=127.0.0.1
export CANVAS_PORT=3000

if lsof -nP -iTCP:"$CANVAS_PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Port $CANVAS_HOST:$CANVAS_PORT is already in use (canvas server may already be running)." >&2
  echo "Open http://127.0.0.1:$CANVAS_PORT or stop the process: lsof -tiTCP:$CANVAS_PORT -sTCP:LISTEN | xargs kill" >&2
  exit 1
fi

echo "Starting Excalidraw canvas server on http://127.0.0.1:3000"
echo "Restart Cursor MCP (excalidraw) after server is up for connected mode."

exec node /opt/homebrew/lib/node_modules/excalidraw-mcp-server/dist/canvas/index.js
