# Skill Reef 🪸🦞

A growing catalog of reusable OpenClaw skills.

## Included skills

- `bottom-feeder` - Knowledge crawling and note synthesis for durable topic/research files.
- `brain-swap` - Fleet-wide OpenClaw model switching across config, sessions, and cron jobs.
- `browser-control` - Decision layer for choosing the right browser-control mode.
- `claude-foreman` - Dispatch heavy coding work to Claude CLI while OpenClaw orchestrates.
- `interactive-sessions` - Design and operate button-driven Telegram/Slack chat sessions, games, wizards, polls, and guided workflows.
- `knowledge-search` - Local semantic knowledge-base search with ChromaDB + Ollama.
- `mermaid` - Mermaid diagram authoring and rendering workflow.
- `moltmaster` - Controlled OpenClaw OAuth/auth-profile refresh operations with dry-run, backups, and provider guardrails.
- `pdf-to-markdown` - Convert PDFs to Markdown with Docling.
- `plugin-creator` - Create, design, review, and troubleshoot OpenClaw plugins, slash commands, message presentation buttons, and interactive handlers.
- `ralph-wiggum` - Bounded iteration loop for small projects and prototypes with verification after each slice.
- `shell-swap` - Mass-switch OpenClaw model settings with codex/gpt/claude lane aliases.
- `shrimp` - Internal pass-through helper for `/shrimp` sub-agent dispatch.
- `telegram-buttons` - Telegram inline button patterns and UX rules.
- `telegram-ui` - Telegram rich chat UI patterns: inline buttons, polls, edits, replies, reactions, media, and pins via OpenClaw.

## Notes

- This repo contains the public-safe subset of the local custom skill library.
- Skills with environment-specific secret references or sensitive local bindings are intentionally omitted.

## Structure

```text
skills/
  <skill-name>/
    SKILL.md
    references/
    scripts/
```

Each skill lives in its own directory so it can be copied or installed cleanly into an OpenClaw workspace.
