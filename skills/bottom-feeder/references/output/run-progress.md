# run-progress

Maintain a per-run progress log separate from knowledge output.

## Location
`knowledge/.runs/<YYYY-MM-DD>-<mode>.md`

Example: `knowledge/.runs/2026-03-30-burn.md`

## Format

```markdown
# Bottom Feeder Run — YYYY-MM-DD (mode)

**Started:** <ISO timestamp>
**Model:** <model used>
**Mode:** routine | burn
**Budget:** <constraint if any>
**Provider lock:** <none | anthropic | openai | venice | ...>
**Provider compliance:** <compliant | violation-blocked>

## Topics

### 1. <Topic Name> — <status: ✅ complete | ⚠️ partial | ❌ skipped>
- **Sources used:** brave, perplexity, ...
- **Output:** `knowledge/topics/<slug>.md`
- **Confidence:** high | medium | low
- **Time spent:** ~Xm
- **Notes:** <anything notable — weak sources, surprising findings, gaps>

### 2. <Topic Name> — ...

## Run Summary
- **Topics attempted:** X
- **Topics complete:** X
- **Topics partial:** X
- **Total sources queried:** X
- **Follow-up candidates:** <topics that need a second pass>
- **Ended:** <ISO timestamp>
```

## Rules
- Update this file AFTER each topic completes (not batched at end)
- If the run is interrupted, the log still reflects everything completed so far
- This file is the audit trail — knowledge files are the deliverables
