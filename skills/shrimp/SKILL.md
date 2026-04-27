---
name: shrimp_skill
description: >
   (Internal) Shrimp skill definition; do not invoke directly from chat.
user-invocable: false
---

# Shrimp 🦐

When invoked via `/shrimp <task>`:

1. Call `sessions_spawn` with:
   - `task`: the user's task (everything after `/shrimp`)
   - `agentId`: "shrimp"
   - `cleanup`: "delete"

2. Say nothing else. The sub-agent announces results when done.

Do NOT analyze, interpret, or add to the task. Pass it through exactly as given.
