#!/usr/bin/env bash
# Source project .env for Excalidraw MCP / canvas server (not for git commit).

load_excalidraw_env() {
  local root="$1"
  local env_file="$root/.env"

  if [[ -f "$env_file" ]]; then
    set -a
    # shellcheck source=/dev/null
    source "$env_file"
    set +a
  fi

  : "${EXCALIDRAW_API_KEY:?Set EXCALIDRAW_API_KEY in .env (copy from .env.example)}"
  export EXCALIDRAW_API_KEY
  export CANVAS_SERVER_URL="${CANVAS_SERVER_URL:-http://127.0.0.1:3000}"
}
