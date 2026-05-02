# Interactive Sessions — Progress

Migrated progress record for the `interactive-sessions` skill. Tracks the evolution of button-driven sessions across Slack and Telegram: games, brainstorms, workflows, wizards.

**Owner:** Clawdia
**Started:** 2026-04-24
**Status:** Active

---

## What This Covers

Interactive multi-step flows delivered via platform-native buttons (Slack Block Kit, Telegram inline keyboards). Not just confirmations — full guided experiences where each tap drives the next step.

### Categories

| Type | Description | Example |
|------|-------------|---------|
| 🧠 Brainstorm Games | Multi-round idea generation with voting | Brainstorm Blitz (2026-04-24) |
| 🎮 Adventure Games | Choose-your-own-adventure style | Cave exploration, mystery solving |
| 🧙 Decision Wizards | Step-by-step structured input collection | Task creation, triage, onboarding |
| 📊 Polls & Surveys | Quick team pulse checks | Sprint retro, feature priority |
| 🔄 Workflows | Guided multi-step business processes | PR review flow, release checklist |

---

## Design Principles (from Brainstorm Blitz v1)

1. **One question per message** — don't overload
2. **Acknowledge the choice before the next step** — show what happened
3. **Add personality to the prompt text** — not sterile menus
4. **Emojis on every button label** — scannable, fun
5. **Telegram: print button options in the message text too** — mobile can truncate/hide full button titles, so include a compact redundant line like `Options: ✅ Approve · ❌ Cancel · ⏰ Later`
6. **Track who picked what** — recap at the end
6. **Include an exit hatch** in flows > 2 steps
7. **Keep rounds short** — 3-4 rounds max before a payoff/summary
8. **Multi-player works** — different people can tap different rounds (Daniel jumped in Round 3!)
9. **End with a deliverable** — summary, saved artifact, or next action

---

## Session History

Substantial sessions get their own reference file in this skill. The table below is the quick index.

| # | Date | Type | Name | Channel | Players | Log |
|---|------|------|------|---------|---------|-----|
| 1 | 2026-04-24 | 🧠 Brainstorm | Brainstorm Blitz v1 | #test-claw | Jared, Daniel | [log](brainstorm-blitz-v1.md) |

---

## Insights & Learnings

Distilled patterns from completed sessions. Updated after each game.

### What Works
- *Fast pacing* — 3 rounds max before a payoff. People lose interest after that.
- *Personality in prompts* — dry menus kill energy; a little edge keeps people clicking.
- *Multi-player naturally* — anyone in the channel can jump in at any round. Track who picked what.
- *End with a deliverable* — summary recap with attributed votes. Makes it feel like it mattered.
- *Emojis on every button* — scannable, fun, non-negotiable.
- *Telegram needs visible option text too* — mobile clients may not show full button labels, so the prompt should include a compact `Options:` line mirroring the buttons.

### What to Improve
- Add a "🃏 Wild Card / write your own" option for creative rounds
- Experiment with a timer or urgency element to raise energy
- Try a scoring system for competitive formats (trivia, "Bug or Feature?")
- Test longer flows (4-5 rounds) with an explicit midpoint checkpoint
- Consider a "spectator recap" message for people who join mid-game

---

## Ideas Backlog

| Idea | Type | Notes |
|------|------|-------|
| "Feature Pitch Roulette" | 🧠 Brainstorm | Random constraint per round (budget, timeline, audience) |
| "Bug or Feature?" | 🎮 Game | Present real edge cases, team votes bug vs feature |
| "Sprint Retro Buttons" | 📊 Poll | What went well / what didn't / action items via buttons |
| "Support Scenario Trainer" | 🧙 Wizard | Present a support ticket, pick the best response |
| "Release Readiness Check" | 🔄 Workflow | Go/no-go checklist with button-driven sign-offs |
| "Crypto Trivia" | 🎮 Game | Quick-fire crypto knowledge quiz with scoring |

---

## Technical Notes

- **Slack research history:** `slack-interactivity.md` — Slack-specific spike, config notes, and patch status
- **Slack rich formatting probe:** `slack-rich-formatting-2026-05-01.md` — normal OpenClaw Slack text vs `MessagePresentation` vs raw Slack `markdown`/`rich_text`/table/checklist rendering
- **Plugin command buttons:** `../../plugin-creator/references/telegram-command-buttons.md` — OpenClaw patterns for `/think`-style command arg menus, plugin `presentation.buttons` + interactive handlers, and `/models`-style custom Telegram pickers; relevant for turning interactive sessions into reusable plugin commands
- **One-shot plugin prompt:** `../../plugin-creator/references/one-shot-extension-prompt.md` — template for generating a minimal OpenClaw extension with a chat slash command
- **Slack skill:** `../slack-ui/SKILL.md` — covers Block Kit buttons, selects, multi-step patterns
- **Telegram skill:** `../telegram-buttons/SKILL.md` — covers inline keyboards
- **Slack button patch required:** `patches/slack-reply-button-wake.md` — enables auto-continuation on button click
- **State management:** Conversation history is the state store (no external DB needed for simple flows)
- **Multi-player:** Works naturally — any channel member can click any button. Track `sender` from inbound metadata.

---

## Changelog

- **2026-05-02:** Added Telegram presentation markup lesson: avoid raw Telegram HTML in `message` + `presentation.blocks` interactive sends unless the exact renderer has been verified
- **2026-05-02:** Added small skill hardening: explicit channel/platform-skill selection, stable callback naming, raw-callback UX repair, and fallback behavior
- **2026-05-02:** Migrated the project into `skills/interactive-sessions/` with this progress file as `references/progress.md`
- **2026-05-02:** Added Telegram mobile readability rule: mirror inline button labels in the message text for interactive sessions
- **2026-05-01:** Logged Slack rich formatting probe: normal message path, `MessagePresentation`, raw Slack `markdown` block, `rich_text`, tables, checklists, and syntax-highlighted code
- **2026-05-01:** Added pointer to plugin command button research for Telegram command menus and picker-style flows
- **2026-04-24:** Added `sessions/` directory and Insights section for historical game logs
- **2026-04-24:** Project created after successful Brainstorm Blitz v1 in #test-claw
