# Telegram Buttons — Local Progress Notes

This file is intentionally git-ignored. Use it for transient implementation notes while improving Telegram button behavior.

## 2026-05-01 — Plugin command button research

Research note created:

- `skills/plugin-creator/references/telegram-command-buttons.md`

Key takeaway: `/think`-style `argsMenu: "auto"` is the cleanest native-command pattern, but current public plugin command types may not expose `argsMenu`. For plugin-owned two-branch choices, use raw slash args or `presentation.buttons` + `api.registerInteractiveHandler(...)`; reserve `/models`-style custom pickers for stateful, multi-step, paginated, or message-editing flows.

Related one-shot prompt/template:

- `skills/plugin-creator/references/one-shot-extension-prompt.md`
