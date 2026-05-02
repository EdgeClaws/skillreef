---
name: plugin-creator
description: Create, design, review, or troubleshoot OpenClaw plugins/extensions, especially plugins that register chat slash commands, use message presentation buttons, or wire interactive handlers. Use when building a new OpenClaw extension, adding an api.registerCommand slash command, creating a one-shot plugin prompt, choosing between raw args vs buttons, or checking plugin SDK docs/source.
---

# Plugin Creator

Use this skill when creating or improving an OpenClaw plugin/extension.

## Fast Path

For a minimal chat slash-command plugin, read `references/one-shot-extension-prompt.md` and adapt the prompt/template to the target plugin.

For Telegram or button branching, read `references/telegram-command-buttons.md` before choosing an implementation pattern. For feasibility and a minimal two-button branching skeleton, read `references/button-branching-feasibility.md`. Remember: Telegram interactive `ctx.respond` is an object (`reply`, `editMessage`, `editButtons`, `clearButtons`, `deleteMessage`), not a callable function.

## Default Workflow

1. **Check current SDK shape first.** Inspect local OpenClaw docs/source before assuming examples are current.
2. **Start boring:** make a working slash command before adding buttons, state, or channel-specific UI.
3. **Use the smallest interaction pattern that works:**
   - raw slash args for simple command branches
   - `presentation.buttons` + `api.registerInteractiveHandler(...)` for plugin-owned button choices; in Telegram callbacks prefer `ctx.respond.editMessage(...)` or `ctx.respond.clearButtons()` over leaving stale buttons behind
   - custom channel-specific callback logic only for stateful pickers/wizards
4. **Verify through the real command path:** plugin loads, command appears/runs, handler returns a valid reply, and button taps route correctly if used.
5. **Document install + usage:** include command examples like `/example plan` and any required config.

## Key Caveats

Built-in OpenClaw native commands like `/think` can use typed command definitions with `argsMenu: "auto"`. Current public plugin command types may not expose that same `argsMenu` field. Do **not** invent unsupported fields; verify `OpenClawPluginCommandDefinition` in the installed SDK. As of the inspected SDK, plugin commands expose metadata such as `name`, `nativeNames`, `nativeProgressMessages`, `description`, `agentPromptGuidance`, `acceptsArgs`, `requireAuth`, `requiredScopes`, `ownership`, and `handler`, but not core-only `args` / `choices` / `argsMenu`.

### Native progress / premessage rotation

Plugin slash commands support `nativeProgressMessages`, but in the current SDK this is command metadata, not a handler-time callback. If you want Tide Pools-style variety, define a local message array plus `pickProgress()` and set `nativeProgressMessages: { default: pickProgress() }` at `api.registerCommand(...)` time. This rotates when command metadata is rebuilt/reloaded, not guaranteed per invocation. Do not claim per-run rotation unless the installed SDK explicitly supports function/array progress values.

## Reference Files

- `references/one-shot-extension-prompt.md` — paste-ready prompt/template for generating a minimal plugin with a chat slash command.
- `references/telegram-command-buttons.md` — implementation research for `/think`-style arg menus, plugin presentation buttons, interactive handlers, and `/models`-style picker callbacks.
- `references/button-branching-feasibility.md` — preliminary feasibility verdict for two-branch plugin buttons, with source evidence and a minimal skeleton.

## Local Docs / Source to Check

Prefer local docs/source first, then live docs for verification. In a repo clone, prefer `docs/plugins/`; in installed environments check project-local `node_modules/openclaw/docs/plugins/`, `/usr/lib/node_modules/openclaw/docs/plugins/`, or `/usr/local/lib/node_modules/openclaw/docs/plugins/` as applicable.

- `docs/plugins/building-plugins.md`
- `/usr/lib/node_modules/openclaw/docs/plugins/building-plugins.md`
- `/usr/local/lib/node_modules/openclaw/docs/plugins/building-plugins.md`
- `/usr/local/lib/node_modules/openclaw/docs/plugins/sdk-entrypoints.md`
- `/usr/local/lib/node_modules/openclaw/docs/plugins/message-presentation.md`
- `/usr/local/lib/node_modules/openclaw/docs/tools/slash-commands.md`
- `/usr/local/lib/node_modules/openclaw/dist/plugin-sdk/src/plugins/types.d.ts`
- `/usr/local/lib/node_modules/openclaw/dist/plugin-sdk/src/auto-reply/reply-payload.d.ts`
- <https://docs.openclaw.ai/plugins/building-plugins>
- <https://docs.openclaw.ai/plugins/sdk-entrypoints>
- <https://docs.openclaw.ai/plugins/message-presentation>
- <https://docs.openclaw.ai/tools/slash-commands>
