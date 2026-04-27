#!/usr/bin/env bash
# Mermaid diagram renderer
# Usage: ./render_mermaid.sh input.mmd output.png

set -euo pipefail

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input.mmd> <output.png>"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"

# Get the directory where this script lives
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PUPPETEER_CONFIG="$SKILL_DIR/references/puppeteer-config.json"

if [ ! -f "$INPUT" ]; then
    echo "Error: Input file '$INPUT' not found"
    exit 1
fi

if [ ! -f "$PUPPETEER_CONFIG" ]; then
    echo "Error: Puppeteer config not found at '$PUPPETEER_CONFIG'"
    exit 1
fi

# Render the diagram
mmdc -i "$INPUT" -o "$OUTPUT" -b transparent -p "$PUPPETEER_CONFIG"

echo "✅ Rendered: $OUTPUT"
