# Plugin Creator — Local Progress Notes

This file is intentionally git-ignored. Use it for transient implementation notes while improving the `plugin-creator` skill.

## 2026-05-01 — Skill promotion

Promoted the plugin-creator project research into a real skill:

- `skills/plugin-creator/SKILL.md`
- `skills/plugin-creator/references/one-shot-extension-prompt.md`
- `skills/plugin-creator/references/telegram-command-buttons.md`

Original project seed was removed after promotion so the source of truth is the skill.

Important finding: built-in `/think` command menus use `argsMenu: "auto"`, but current public plugin command types may not expose `argsMenu`. Plugin-owned choices should verify SDK types and usually use raw slash args or `presentation.buttons` + `api.registerInteractiveHandler(...)`.

## 2026-05-01 — Button branching feasibility

Added `references/button-branching-feasibility.md`.

Verdict: Telegram two-button plugin branching is feasible today via `presentation.buttons` + `api.registerInteractiveHandler(...)`. Public plugin commands do not currently expose typed `args` / `argsMenu`, so `/think`-style automatic native arg menus are not currently available to plugin authors unless the SDK changes. Next useful proof: build `/branchdemo`, send two buttons, verify callback dispatch and edit/clear behavior in Telegram.

## 2026-05-02 — Foreman review corrections

Merged review findings into the packaged skill:

- Corrected Telegram interactive response guidance: `ctx.respond` is an object with methods (`reply`, `editMessage`, `editButtons`, `clearButtons`, `deleteMessage`), not a callable function.
- Button callbacks should usually edit or clear the original button message to avoid stale buttons.
- Telegram callback data limit is 64 bytes; use compact namespaced values and server-side state for larger payloads.
- Documented `{ handled: true }` vs `{ handled: false }` semantics for plugin interactive handlers.
- Broadened local docs path guidance beyond `/usr/local` to include repo docs and `/usr/lib` installs.
