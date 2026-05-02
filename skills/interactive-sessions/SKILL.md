---
name: interactive-sessions
description: Design, run, migrate, document, or improve interactive button-driven chat sessions: multi-step Telegram inline-keyboard flows, Slack Block Kit/button/select flows, games, brainstorms, decision wizards, polls, surveys, and workflow assistants. Use when creating or operating guided chat experiences where each user tap/selection drives the next prompt, especially cross-platform Telegram/Slack sessions.
---

# Interactive Sessions

Use this skill for multi-step, button-driven chat experiences: games, brainstorms, wizards, polls, surveys, and guided workflows.

This is the high-level orchestration skill. For platform mechanics, also use:
- Telegram: `skills/telegram-ui/SKILL.md`
- Slack: `skills/slack-ui/SKILL.md`
- Shared formatting source of truth: `knowledge/procedures/platform-message-formatting.md`

## Fast Classifier

Use interactive sessions when the user wants any of these:
- a button-driven game or choose-your-own-adventure flow
- a brainstorm with rounds, voting, or recap
- a decision wizard or intake workflow
- a multi-step poll/survey/checklist
- reusable chat UX patterns across Telegram, Slack, or future channels

Do not use it for a single confirmation unless the prompt is part of a larger flow; use the platform button skill directly instead.

## Core Session Pattern

1. Define the session goal and payoff.
2. Identify the channel and load the platform skill if needed: Slack → `slack-ui`, Telegram → `telegram-ui`.
3. Keep each turn to one question or decision.
4. Offer 2–6 tap-friendly options.
5. Send platform-native controls, not fake text buttons.
6. Acknowledge the selected choice before the next step.
7. Track state in the conversation unless persistence is explicitly required.
8. End with a useful deliverable: recap, decision, artifact, task, or next action.

## Design Rules

- Keep rounds short: 3–4 rounds before a payoff or checkpoint.
- Put personality in prompts; sterile menus kill momentum.
- Use emojis on button labels for scanability.
- Include an exit hatch in flows longer than 2 steps.
- In group chats, track who chose what and recap attribution when useful.
- Multi-player is allowed by default: any participant may tap unless the flow says otherwise.
- For creative sessions, consider a `🃏 Wild Card / write your own` option.
- Use stable callback values: lowercase snake_case, scoped to the flow when helpful, e.g. `pd_edgespend`, `triage_bug`, `cancel`.
- Never expose raw callback values as the primary UX. If a callback token appears in chat, translate it back into the human-readable choice and continue.

## Telegram-Specific Rule

On Telegram, always mirror button options in the message text because mobile may truncate or hide full button titles.

Pattern:

```text
Pick a lane 👇

Options: ✅ Approve · ❌ Cancel · ⏰ Later
```

Then send the same choices as real inline buttons using the Telegram button path. Do not make the text list the only control.

When using `message` with `presentation.blocks`, keep the visible text plain/portable. Do not mix Telegram HTML tags like `<b>...</b>` into the top-level message or presentation text unless you have verified that exact send path parses them. For emphasis in interactive sessions, prefer plain labels, bullets, emoji, or short headings over raw markup.

## Slack-Specific Rule

Use Slack-native buttons/selects through the available Slack UI path. Keep fallback text readable, and prefer `MessagePresentation` when a portable abstraction is enough. For deeper Slack rendering/interaction details, read the Slack references below.

## Failure / Fallback Rule

If native controls fail, are invisible, or return awkward raw callback text:
1. Acknowledge briefly.
2. Restate the human-readable options in plain text.
3. Continue from the user's typed/callback choice if clear.
4. Fix the platform-specific skill/doc after the session if the failure revealed a reusable issue.

## Reference Files

Load only what you need:

- `references/progress.md` — migrated progress doc, project status, design principles, backlog, and changelog.
- `references/slack-interactivity.md` — Slack-specific interaction spike, config notes, and button wake history.
- `references/slack-rich-formatting-2026-05-01.md` — Slack rich formatting probe and rendering findings.
- `references/brainstorm-blitz-v1.md` — first completed session log and lessons.

## Maintenance

When an interactive session teaches a reusable lesson:
1. Update `references/progress.md`.
2. Add or update a session log reference if the flow was substantial.
3. Promote platform-specific findings to the relevant platform skill (`telegram-ui` or `slack-ui`) and to `knowledge/procedures/platform-message-formatting.md` when broadly applicable.
