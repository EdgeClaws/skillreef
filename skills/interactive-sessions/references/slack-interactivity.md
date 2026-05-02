# Slack Interactivity Research

**Status:** ✅ Working locally
**Project:** Interactive Sessions
**Scope:** Slack-specific technical history for buttons, selects, and multi-step game flows.

This started as a standalone `projects/slack-interactive-games/` spike. It now lives under `projects/interactive-sessions/` because the real work is broader than Slack-only games.

## Outcome
- Slack interactive replies were enabled in OpenClaw config on 2026-04-22.
- Agent-authored buttons via `[[slack_buttons: ...]]` are working.
- Agent-authored selects via `[[slack_select: ...]]` are supported syntactically.
- Multi-step button flows now auto-continue after clicks.
- `MessagePresentation` buttons and selects were validated in Slack DMs on 2026-05-01; both delivered callbacks.
- Raw Slack Block Kit `markdown` and `rich_text` blocks can render rich Slack-native output: headers, tables, checklists, quotes, and language-tagged code blocks.
- The current Slack setup is good enough for lightweight games, brainstorms, polls, decision trees, and polished Slack-native workflow cards.

## Current Capability Snapshot
- Button rendering: ✅
- Button click callback: ✅
- Select rendering: ✅
- Select callback delivery: ✅ validated in Slack DM 2026-05-01
- Auto-continuation after click: ✅, with local patch
- Multi-step game loops: ✅
- `MessagePresentation` cards/buttons/selects: ✅ validated in Slack DM 2026-05-01
- Slack-native rich formatting (`markdown`/`rich_text` blocks): ✅ validated in Slack DM 2026-05-01
- Thread-scoped flows: ⚠️ not fully validated

## Key Config
```json5
{
  "channels": {
    "slack": {
      "capabilities": {
        "interactiveReplies": true
      }
    }
  }
}
```

## Root Cause We Hit
Slack button clicks were reaching OpenClaw, but the assistant was not always getting a follow-up turn. The gap was in the Slack block-action path: it queued the interaction event but did not route it back through the normal inbound-message flow.

## Local Fix
A local patch now converts reply-button clicks into synthetic inbound Slack messages, which lets the assistant continue the flow immediately. That makes Slack behave much closer to Telegram's callback handling pattern.

## Validation History
- **2026-05-01:** validated `MessagePresentation` card/buttons/select in Slack DM; button callback `showcase_chaos` and select callback `qa_triage` both reached the assistant.
- **2026-05-01:** validated raw Slack Block Kit `markdown` + `rich_text` payloads; Slack rendered real header/table/checklist/quote/language-code output. See `slack-rich-formatting-2026-05-01.md`.
- **2026-04-21:** confirmed Slack-side support and started the original research spike
- **2026-04-22:** enabled interactive replies in config
- **2026-04-22:** confirmed button render + click callback round-trip
- **2026-04-22:** identified the missing auto-continuation bug
- **2026-04-22:** validated the local synthetic-message patch
- **2026-04-23:** ran a 3-round test game in `#test-claw` successfully end to end

## Important Files
- `slack-rich-formatting-2026-05-01.md`
- `../../patches/slack-reply-button-wake.md`
- `../../patches/check-slack-button-patch.sh`
- `../../skills/slack-ui/SKILL.md`
- `../sessions/001-brainstorm-blitz-v1.md`

## Operational Note
After `openclaw update`, rerun `bash patches/check-slack-button-patch.sh` until the upstream fix lands.
