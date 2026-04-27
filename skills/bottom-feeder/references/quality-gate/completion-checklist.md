# completion-checklist

Before advancing to the next topic, verify the current topic's output passes ALL checks:

## Required sections (knowledge/topics file)
- [ ] Summary — ≥3 sentences, no placeholders
- [ ] Current State — concrete facts with dates, not vague
- [ ] Why It Matters — tied to the user's ecosystem/work, not generic
- [ ] Open Questions — at least 1 genuine unknown
- [ ] Sources — at least 2 dated sources (URL + date accessed)

## Required metadata (YAML header)
- [ ] `confidence` set to low/medium/high (not omitted)
- [ ] `sources_used` lists actual tools used (not assumed)

## Quality gates
- [ ] No "TODO" or "TBD" left in body
- [ ] If confidence is `low`, note WHY (source scarcity? contradictory info?)
- [ ] File is self-contained — a reader with no context can understand it
- [ ] If run policy has a provider lock, this topic was produced using the locked provider only

## Failure behavior
- If a section can't be filled: write it with an explicit `[INCOMPLETE: reason]` tag
- Do NOT skip the topic — partial with honesty beats moving on silently
- Log the gap in the run progress file for follow-up
