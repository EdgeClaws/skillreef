# hardcoded-list

Read `config/topics.md`.

Rules:
- Treat each bullet as candidate topic.
- Prefer topics not crawled in last 7 days.
- If `config/next-topic.md` exists, that topic wins unless user overrides.
- Normalize topic to a short slug candidate for output filename.
