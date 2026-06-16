#!/usr/bin/env bash
# MCP stdio entry: load .env then exec excalidraw-mcp-server (connected mode).

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=scripts/load_excalidraw_env.sh
source "$ROOT/scripts/load_excalidraw_env.sh"
load_excalidraw_env "$ROOT"

exec /opt/homebrew/bin/excalidraw-mcp-server
