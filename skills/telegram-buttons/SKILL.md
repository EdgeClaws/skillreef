---
name: telegram-buttons
description: >
   For using buttons in Telegram
---
# Telegram Inline Buttons

Use this skill whenever sending a button prompt on Telegram. Buttons replace "would you like me to proceed?" text.

**Default rule:** if you're offering **2 to 6 discrete options** and the user can answer by tapping one, send buttons instead of a plain text menu.

**Non-negotiable backstop:** before sending any Telegram reply that includes a choice, run this quick check:
1. Am I only informing them? → plain text
2. Do they need to type something custom? → plain text
3. Can they answer by tapping 1 of 2 to 6 options? → buttons, mandatory

If you have already drafted a bullet list, numbered list, or "pick a lane" style reply and the user is meant to choose one option, do **not** send it as text. Convert it to buttons first.

---

## Setup

This skill depends on a matching `AGENTS.md` house rule so the behavior stays active by default.

**Keep the split clean:**
- `AGENTS.md` = short policy + fast backstop
- `skills/telegram-buttons/SKILL.md` = playbook, examples, repair flow, and button patterns

Use this compact `AGENTS.md` block:

```markdown
## Telegram Inline Buttons

On Telegram, use inline buttons instead of asking "would you like me to proceed?" in plain text.

**Hard rule:** if the user can answer by tapping one of **2 to 6 discrete options**, use inline buttons instead of a plain text menu.

This includes confirmations, "pick a lane" prompts, and short idea menus like "here are 3 ideas, pick one."

**Fast backstop:**
- Pure info → plain text
- Open input needed → plain text
- 2 to 6 discrete choices → buttons

Do **not** send numbered or bulleted pick-one menus on Telegram when buttons would work.

See `skills/telegram-buttons/SKILL.md` for button patterns, repair behavior, and implementation details.
```

No plugins required. Use the native `message` tool with Telegram buttons and, when helpful, `message edit` to reflect the selected choice.

---

## Decision Rule

Use this quick classifier before choosing the reply path:

- **Pure info** → plain text reply
- **Open-ended input needed** → plain text reply
- **2 to 6 discrete tap-friendly options** → send Telegram buttons

Important: a conversational suggestion list still counts as a menu if the user is being asked to pick from it.

That includes common misses like:
- "Here are 3 ideas"
- "Three good lanes"
- "Pick a lane"
- "Which one do you want me to do?"
- "Want A, B, or C?"

---

## Sending Buttons

When in doubt, prefer sending the button prompt directly instead of writing a normal chat reply first and "maybe" adding buttons later. The menu itself should be the button message.

```bash
openclaw message send \
  --channel telegram \
  -t <chat_id> \
  --message "Question text" \
  --buttons '<json_grid>'
```

**Save the returned message ID** — you'll need it to edit the message after a tap.

---

## Emoji Rule

**Always use emojis on button labels.** They make buttons visually scannable and feel natural in chat.

**Also add light emoji flavor to the prompt text when sending a menu.** If the user is choosing between a few options, the lead-in should feel warm and alive, not sterile. Good pattern: a short prompt line plus 1 fitting emoji, for example `Pick a lane 🦞`, `Choose a move 👇`, or `What are we feeling today? 😌`.

Use restraint:
- 1 emoji in the prompt line is usually enough
- match the mood and intent
- don't force emojis into serious/sensitive prompts
- button labels should stay short and scannable

Pick emojis that match intent:

| Intent | Emoji |
|--------|-------|
| Yes / Approve / Proceed | ✅ |
| No / Cancel / Stop | ❌ |
| Later / Defer / Snooze | ⏰ |
| Always / Lock in | 🔒 |
| Danger / Destructive | ⚠️ |
| Info / More details | ℹ️ |
| Neutral option A/B | 🅰️ 🅱️ or a relevant icon |

---

## Button Grid Layouts

### Binary (Y/N) — same row
```json
[[{"text":"✅ Yes","callback_data":"yes"},{"text":"❌ No","callback_data":"no"}]]
```

### Binary with defer — two rows
```json
[
  [{"text":"✅ Do it","callback_data":"yes"},{"text":"❌ Cancel","callback_data":"no"}],
  [{"text":"⏰ Not now","callback_data":"defer"}]
]
```

### Three choices
```json
[
  [{"text":"🅰️ Option A","callback_data":"a"},{"text":"🅱️ Option B","callback_data":"b"}],
  [{"text":"🔀 Option C","callback_data":"c"}]
]
```

### Multi-choice stacked
```json
[
  [{"text":"🔥 Do it now","callback_data":"now"}],
  [{"text":"⏰ Remind me later","callback_data":"later"}],
  [{"text":"❌ Cancel","callback_data":"cancel"}]
]
```

---

## Missed It? Repair Fast

If you realize you already sent a plain-text Telegram menu that should have been buttons:
- acknowledge it briefly
- resend the same choice as buttons immediately
- do not defend the mistake or leave the user to type the option unless they already did

Example repair:
- `You're right, that should've been buttons. Pick a lane 👇`
- then send the button menu

## After a Button Is Tapped

The tap arrives as a new message containing the `callback_data` value. Handle it and proceed.

For lightweight interactive games, keep the callback payload stateless and descriptive enough that a later turn can still be handled cleanly. Good pattern: `game_slug_scene_choice` or another self-describing token, instead of assuming the reply arrives immediately or that short-lived in-memory state still exists.

When the game is turn-based in chat:
- include a short plain-text option list under the buttons so mobile users can read the full choices even if button labels are clipped
- keep button labels compact, but make the body text flavorful enough to carry the fantasy, stakes, or genre hook
- treat each callback as a fresh re-entry point, not proof that the user answered "on time"
- avoid flows that break if multiple people vote or if the next choice happens much later

**Optional — edit the original message** to remove buttons and show the selection visually (nice UX, but skip it if it would complicate the flow):

```bash
openclaw message edit \
  --channel telegram \
  -t <chat_id> \
  --message-id <original_message_id> \
  --message "Want me to create that Asana task now?\n\n✅ Do it — selected"
```

If you do edit, use these emoji commit indicators:
- ✅ / 🟩 = approved / yes / proceed
- 🟥 = no / cancelled
- ⬛ = deferred / skipped

**Never block the action waiting to edit** — proceed with what the user selected regardless.

---

## Stale & Duplicate Callbacks

- If a callback arrives after the message was already edited (buttons removed), **silently ignore it** — no extra message, no extra edit
- Button prompts don't persist across sessions — if a prompt was never answered before a session ended, treat any late tap as stale and ignore

---

## 🔮 Future Improvements

> **Not implemented yet — logged for future development.**

### 1) Runtime backstop for missed menus

Best reliability upgrade: detect Telegram replies that look like a menu, for example numbered options or short bullet-choice lists, and warn or block unless the reply is sent through a button-capable path.

Why this matters:
- prompt instructions are easy to forget in conversational turns
- this catches misses without requiring a second full reasoning pass on every message
- it turns the rule into enforcement instead of preference

### 2) Lightweight classifier before send

A very small classifier could label candidate replies as:
- info
- open input
- discrete choice

Only the third class would route to buttons. This is cheaper than a full reflective pre-send review, but still adds some overhead, so it should stay lightweight if implemented.

### 3) Gateway-level callback hook

The cleanest long-term UX solution is a plugin hook that intercepts button callbacks at the gateway level and auto-edits the message *without* triggering an LLM turn. This would mean:
- Zero token cost for the visual cleanup
- Instant button removal on tap (no round-trip to the model)
- Same pattern `telegram-approval-buttons` uses for exec approvals

To build: a plugin that listens for Telegram `callback_query` events, matches them against a registry of pending button messages, auto-edits the message, then forwards the selection to the agent as a normal message. Would require a small in-memory store (message ID → pending prompt) and the Telegram Bot API `editMessageReplyMarkup` call.

Reference: `telegram-approval-buttons` plugin does this for exec approvals — same architecture, broader scope.

---

## Rules

- **Max ~6 buttons** — more than that, summarize and let the user pick
- **Labels: 1–4 words** — short and scannable
- **Prompt copy should feel human** — avoid dry lead-ins like `Pick a lane:` unless the situation is intentionally formal; prefer a little personality and, when it fits, a light emoji
- **Always include an escape hatch** when appropriate: "Not now", "Cancel", "Skip"
- **`callback_data`** = what comes back when tapped — use a clear, meaningful keyword
- **For game/story flows, make `callback_data` stateless and scene-descriptive** so late replies still work
- **When button text may clip on mobile, print the numbered options in plain text too**
- **One button prompt per message** — don't stack multiple questions
- Use `--reply-to <message_id>` when buttons are a direct response to a specific message
- **A 2 to 6 option choice on Telegram is a buttons problem, not a prose problem**
- **Do not ask the user to type "1", "2", or "3" when buttons would work**
- **If you catch the miss before send, rewrite; if you catch it after send, repair immediately with buttons**

---

## Known Chat IDs

| Person | ID |
|--------|----|
| Jared (primary) | `6566057320` |

---

## Full Example — Confirm before acting

```bash
# Step 1: Send with buttons (capture message ID from output)
openclaw message send \
  --channel telegram \
  -t 6566057320 \
  --message "Want me to create that Asana task now?" \
  --buttons '[[{"text":"✅ Yes, do it","callback_data":"yes"},{"text":"❌ Not yet","callback_data":"no"}]]'

# Step 2: After tap received — edit to commit selection
openclaw message edit \
  --channel telegram \
  -t 6566057320 \
  --message-id <returned_id> \
  --message "Want me to create that Asana task now?\n\n✅ Yes, do it — selected"

# Step 3: Proceed with the action
```
