# conversation-mining

Mine recent context for candidate topics:
- `memory/daily/YYYY-MM-DD.md` (today + yesterday)
- current conversation requests

Extract:
- repeated themes
- explicit asks ("research X", "build plan for Y")
- unresolved questions

Score boost when:
- mention count >= 2
- appears time-sensitive
- aligns with configured interest areas
