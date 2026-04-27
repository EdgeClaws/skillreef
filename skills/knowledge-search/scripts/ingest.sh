#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_DIR="$(cd "$SKILL_DIR/../.." && pwd)"
DEFAULT_SOURCE_DIR="$WORKSPACE_DIR/knowledge"

if [ ! -d "$DEFAULT_SOURCE_DIR" ] && [ -d "$SKILL_DIR/data" ]; then
    DEFAULT_SOURCE_DIR="$SKILL_DIR/data"
fi

export SOURCE_DIR="${SOURCE_DIR:-${DATA_DIR:-$DEFAULT_SOURCE_DIR}}"
export CHROMA_PERSIST_DIR="${CHROMA_PERSIST_DIR:-$HOME/.openclaw/chroma/knowledge-search}"
export CHROMA_COLLECTION="${CHROMA_COLLECTION:-knowledge}"
export OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"
export EMBEDDING_MODEL="${EMBEDDING_MODEL:-nomic-embed-text}"
export CHUNK_SIZE="${CHUNK_SIZE:-1500}"
export CHUNK_OVERLAP="${CHUNK_OVERLAP:-200}"

exec python3 "${SCRIPT_DIR}/ingest_runner.py" \
    "$SOURCE_DIR" "$CHROMA_PERSIST_DIR" "$CHROMA_COLLECTION" \
    "$OLLAMA_URL" "$EMBEDDING_MODEL" "$CHUNK_SIZE" "$CHUNK_OVERLAP"
