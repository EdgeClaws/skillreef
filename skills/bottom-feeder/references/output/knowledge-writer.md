# knowledge-writer

Write one file per topic immediately after synthesis.

Primary destination:
- `knowledge/topics/<topic-slug>.md`

Deep-dive destination:
- `knowledge/research/<YYYY-MM-DD>-<topic-slug>.md`

Include YAML header:
- title
- crawled (ISO timestamp)
- mode (routine|burn)
- sources_used
- estimated_cost_units (optional, provider-agnostic relative cost)
- estimated_cost_diem (optional, legacy Venice compatibility)
- confidence (low|medium|high)

Body sections (recommended):
1. Summary
2. Current State
3. Why It Matters (for our ecosystem)
4. Open Questions
5. Sources
