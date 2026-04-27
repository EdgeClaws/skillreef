#!/usr/bin/env bash
set -euo pipefail

# Bottom Feeder helper: extract a spend budget number from JSON.
# Accepts either direct balance JSON or provider-usage snapshot JSON.
# Supports these fields (first match wins):
#   .remaining | .balance | .credits | .venice.data.diem
# Also tolerates noisy preamble text by parsing from first '{'.

input="${1:-}"
if [[ -n "$input" ]]; then
  data="$(cat "$input")"
else
  data="$(cat)"
fi

python3 - <<'PY' "$data"
import json,sys
raw=sys.argv[1]

# Tolerate log/preamble lines before JSON
i = raw.find('{')
if i >= 0:
    raw = raw[i:]

obj=json.loads(raw)

def pick(o, path):
    cur=o
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur=cur[k]
    return cur

candidates=[
    pick(obj,["remaining"]),
    pick(obj,["balance"]),
    pick(obj,["credits"]),
    pick(obj,["venice","data","diem"]),
]
val=next((c for c in candidates if c is not None), None)
if val is None:
    raise SystemExit("Unable to determine balance from input JSON")
print(f"{float(val):.4f}")
PY
