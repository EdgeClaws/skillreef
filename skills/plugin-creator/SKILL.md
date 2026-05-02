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

## Manifest Best Practices (`openclaw.plugin.json`)

Every plugin needs a manifest. Beyond `id`, `name`, `description`, and `configSchema`, these fields matter for performance and correct activation:

### `activation.onStartup` (required for all new plugins)

OpenClaw is moving away from implicit startup loading. Every plugin should declare this explicitly:

```json
{
  "activation": { "onStartup": false }
}
```

- `false` — plugin is lazy-loaded on demand (slash commands, tools, hooks). **Use this for most plugins.**
- `true` — plugin must import during Gateway startup (channel adapters, startup HTTP routes, gateway methods needed before listen).

Without this field, the plugin falls back to the deprecated implicit startup sidecar, which loads eagerly and adds unnecessary startup/per-turn overhead. `openclaw doctor` will flag plugins missing this field.

### `activation` — narrower triggers

Beyond `onStartup`, the activation block supports targeted triggers so the loader only imports your plugin when relevant:

```json
{
  "activation": {
    "onStartup": false,
    "onCommands": ["mycommand"],
    "onProviders": ["myprovider"],
    "onChannels": ["mychannel"]
  }
}
```

Available: `onCommands`, `onProviders`, `onChannels`, `onAgentHarnesses`, `onRoutes`, `onConfigPaths`, `onCapabilities`.

### Side-effect guarding with `api.registrationMode`

OpenClaw calls `register(api)` during both discovery (read-only scan) and full activation. Guard expensive work:

```ts
register(api) {
  api.registerCommand({ name: "mycommand", ... });

  if (api.registrationMode !== "full") return;

  // Only run during live activation — not during discovery scans
  startBackgroundWorker();
  openDatabase();
}
```

Modes: `"full"` (live runtime), `"discovery"` (read-only scan), `"setup-only"`, `"setup-runtime"`, `"cli-metadata"`.

### Other manifest fields to know

| Field | When to use |
|-------|-------------|
| `enabledByDefault` | Bundled plugins only. Omit for external plugins. |
| `providerAuthEnvVars` | Map provider id to env var names for cheap auth detection without runtime import. Deprecated in favor of `setup.providers[].envVars`. |
| `contracts.tools` | Declare tool ids for manifest-driven discovery without importing runtime. |

### `package.json` — `setupEntry` and deferred loading

For **channel plugins** that register HTTP routes or gateway methods at startup, consider a lightweight `setupEntry`:

```json
{
  "openclaw": {
    "extensions": ["./index.ts"],
    "setupEntry": "./setup-entry.ts",
    "startup": {
      "deferConfiguredChannelFullLoadUntilAfterListen": true
    }
  }
}
```

`setupEntry` loads instead of the full entry during startup/setup. Only enable deferred loading when `setupEntry` covers all pre-listen capabilities. Not needed for simple command plugins.

## Key Caveats

Built-in OpenClaw native commands like `/think` can use typed command definitions with `argsMenu: "auto"`. Current public plugin command types may not expose that same `argsMenu` field. Do **not** invent unsupported fields; verify `OpenClawPluginCommandDefinition` in the installed SDK. As of the inspected SDK, plugin commands expose metadata such as `name`, `nativeNames`, `nativeProgressMessages`, `description`, `agentPromptGuidance`, `acceptsArgs`, `requireAuth`, `requiredScopes`, `ownership`, and `handler`, but not core-only `args` / `choices` / `argsMenu`.

### Native progress / premessage rotation

Plugin slash commands support `nativeProgressMessages`, but in the current SDK this is command metadata, not a handler-time callback. If you want Tide Pools-style variety, define a local message array plus `pickProgress()` and set `nativeProgressMessages: { default: pickProgress() }` at `api.registerCommand(...)` time. This rotates when command metadata is rebuilt/reloaded, not guaranteed per invocation. Do not claim per-run rotation unless the installed SDK explicitly supports function/array progress values.

## Reference Files

- `references/one-shot-extension-prompt.md` — paste-ready prompt/template for generating a minimal plugin with a chat slash command.
- `references/telegram-command-buttons.md` — implementation research for `/think`-style arg menus, plugin presentation buttons, interactive handlers, and `/models`-style picker callbacks.
- `references/button-branching-feasibility.md` — preliminary feasibility verdict for two-branch plugin buttons, with source evidence and a minimal skeleton.

## Local Docs / Source to Check

Prefer local docs/source first, then live docs for verification. The global install path varies by system — check both `/usr/lib/node_modules/openclaw/` and `/usr/local/lib/node_modules/openclaw/`. In a repo clone, prefer `docs/plugins/`.

- Local docs (check whichever global path exists):
  - `{OPENCLAW_ROOT}/docs/plugins/building-plugins.md`
  - `{OPENCLAW_ROOT}/docs/plugins/sdk-entrypoints.md`
  - `{OPENCLAW_ROOT}/docs/plugins/message-presentation.md`
  - `{OPENCLAW_ROOT}/docs/tools/slash-commands.md`
- Local SDK types:
  - `{OPENCLAW_ROOT}/dist/plugin-sdk/src/plugins/types.d.ts`
  - `{OPENCLAW_ROOT}/dist/plugin-sdk/src/plugins/manifest.d.ts`
  - `{OPENCLAW_ROOT}/dist/plugin-sdk/src/auto-reply/reply-payload.d.ts`
- Live docs:
  - <https://docs.openclaw.ai/plugins/building-plugins>
  - <https://docs.openclaw.ai/plugins/sdk-entrypoints>
  - <https://docs.openclaw.ai/plugins/message-presentation>
  - <https://docs.openclaw.ai/plugins/sdk-setup>
  - <https://docs.openclaw.ai/plugins/architecture-internals>
  - <https://docs.openclaw.ai/tools/slash-commands>

Where `{OPENCLAW_ROOT}` is the first that exists of `/usr/lib/node_modules/openclaw`, `/usr/local/lib/node_modules/openclaw`, or a project-local `node_modules/openclaw`.


## WatchCatfish Pattern: Button-Steered Slash Command, No LLM

For simple plugin command steering like `/health` → Hardware/Services, prefer the **button-steered slash-args pattern** before building a full interactive state machine:

1. Register one command with `acceptsArgs: true`.
2. With no args, return a small menu.
3. On Telegram, return `channelData.telegram.buttons` rows with `callback_data` set to the exact slash command branch, e.g. `/health hardware`.
4. Implement the branch as ordinary slash-arg handling (`hardware` → `core`, `services` → `services`).
5. Keep the branch implementation token-free/no-LLM by doing all work inside the plugin handler/probe.
6. For non-Telegram fallback, include plain text commands: `Run /health hardware or /health services.`

Minimal Telegram menu shape from WatchCatfish:

```ts
return {
  text: [
    "🐟 WatchCatfish · Health",
    "Choose a token-free report 👇",
    "",
    "Options: 🖥️ Hardware · 🧰 Services"
  ].join("\n"),
  channelData: {
    telegram: {
      buttons: [[
        { text: "🖥️ Hardware", callback_data: "/health hardware", style: "primary" },
        { text: "🧰 Services", callback_data: "/health services", style: "success" }
      ]]
    }
  }
};
```

Use this when a button can safely rerun the same command with a short argument. Use `presentation.buttons` + `api.registerInteractiveHandler(...)` when the plugin owns custom callback state, needs edit-in-place behavior, or the callback value is not itself a command. Use a `/models`-style custom picker only for pagination/back/stateful menus.
