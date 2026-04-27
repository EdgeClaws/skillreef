#!/usr/bin/env bash
set -euo pipefail

# Optional Tide Pools hook for Bottom Feeder.
# Output: JSON snapshot of provider usage + Venice augmentation.

CORE_CLI="${TIDE_POOL_CLI:-$HOME/.openclaw/extensions/tide-pools/cli.mjs}"
LEGACY_CLI="${LOBSTER_USAGE_CLI:-$HOME/.openclaw/extensions/lobster-usage/cli.mjs}"

if [[ -f "$CORE_CLI" ]]; then
  node "$CORE_CLI" --format json
  exit 0
fi
if [[ -f "$LEGACY_CLI" ]]; then
  node "$LEGACY_CLI" --format json
  exit 0
fi

# Fallback if optional package isn't installed.
notice="tide-pools plugin not found at ${CORE_CLI} (legacy checked: ${LEGACY_CLI}); using fallback openclaw status (no Venice augmentation)."
raw="$(openclaw status --usage --json 2>/dev/null || true)"
if [[ -z "$raw" ]]; then
  printf '{"generatedAt":null,"providers":[],"statusError":"openclaw status failed","venice":null,"notice":%s}\n' "$(python3 - <<'PY' "$notice"
import json,sys
print(json.dumps(sys.argv[1]))
PY
)"
  exit 0
fi

python3 - <<'PY' "$raw" "$notice"
import json,sys
raw=sys.argv[1]
notice=sys.argv[2]
i=raw.find('{')
if i<0:
    print(json.dumps({
      "generatedAt": None,
      "providers": [],
      "statusError": "status JSON parse failed",
      "venice": None,
      "notice": notice,
    }))
    raise SystemExit(0)
obj=json.loads(raw[i:])
out={
  "generatedAt": None,
  "providers": obj.get("usage",{}).get("providers",[]),
  "statusError": None,
  "venice": None,
  "notice": notice,
}
print(json.dumps(out))
PY
