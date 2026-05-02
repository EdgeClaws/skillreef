# Slack Rich Formatting Probe — 2026-05-01

**Project:** Interactive Sessions  
**Channel:** Slack DM with Jared Pearson  
**Status:** ✅ Raw Slack rich formatting works; docs need nuance

## Why this probe happened

Jared noticed the Slack output was getting much richer than our conservative formatting rules implied. We tested normal OpenClaw Slack replies, OpenClaw `MessagePresentation`, and raw Slack Block Kit payloads to understand what is actually possible.

## Resources checked

Official Slack docs:
- Slack message formatting: https://docs.slack.dev/messaging/formatting-message-text/
- Slack markdown block: https://docs.slack.dev/reference/block-kit/blocks/markdown-block/
- Slack rich text block: https://docs.slack.dev/reference/block-kit/blocks/rich-text-block/
- Slack Block Kit blocks/actions/select/button references from the platform-formatting cleanup pass

OpenClaw docs/files:
- `/usr/local/lib/node_modules/openclaw/docs/concepts/markdown-formatting.md`
- `/usr/local/lib/node_modules/openclaw/docs/channels/slack.md`
- `/usr/local/lib/node_modules/openclaw/docs/plugins/message-presentation.md`
- `knowledge/procedures/platform-message-formatting.md`
- `skills/slack-ui/SKILL.md`
- `skills/slack/SKILL.md`

## What we sent

### Test 1 — normal Slack/OpenClaw text path

Sent through the first-class `message` tool as a normal Slack message.

Content included:
- Slack-style bold, italic, strike
- inline code
- nested-ish bold/italic combinations
- quote lines
- Slack link syntax
- Slack date token
- ordered pseudo-list
- fenced code block

Observed from screenshots:
- Basic bold / italic / strike rendered correctly.
- Inline code rendered and suppressed inner formatting.
- Nested bold+italic rendered better than expected; the combined span looked sane.
- Date token rendered as localized Slack date/time.
- Slack link syntax rendered as a clickable label.
- Link unfurled by default, producing a docs preview card.
- Code block rendered as a code block, but not with visible language syntax highlighting in this normal path.
- Block quote behavior was imperfect: first quoted line showed the quote bar, second line appeared less clearly quoted. Needs a targeted quote-only retest.

### Test 2 — OpenClaw `MessagePresentation`

Sent through the first-class `message` tool with `presentation` containing:
- title
- info tone
- text block
- context block
- divider
- buttons
- select menu

Observed from screenshots:
- Slack rendered a clean card-like message.
- Buttons rendered as colored Slack buttons:
  - success / green
  - neutral-ish
  - danger / red
- Select menu rendered and was usable-looking.
- A warning triangle appeared next to the select after selection/render. Needs follow-up: could be Slack client state, select payload shape, or missing/odd callback metadata.

### Test 3 — raw Slack Block Kit `markdown` block + `rich_text` block

Sent directly through Slack `chat.postMessage` with raw `blocks` to push beyond the normal assistant path.

Raw markdown block included:
- `#` header
- real Markdown bold/italic variants
- nested bold+italic
- Markdown-style link
- task list checkboxes
- Markdown table
- fenced Python code block

Raw rich_text block included:
- styled spans
- quote element
- bullet list
- inline code-style text

API result:
- `ok: true`
- Slack accepted the payload and returned only `missing_charset` warning.

Observed from API readback and screenshots:
- Slack transformed the `markdown` block into multiple native blocks.
- Header became a real `header` block.
- Markdown table became an actual Slack `table` block.
- Task list became checklist-style rich text with checkboxes.
- Checked task rendered struck-through with checkbox checked.
- Fenced Python code became a preformatted block with `language: python`.
- Raw `rich_text` quote and bullet list rendered correctly.
- The Markdown docs link unfurled, so raw Slack posts may need `unfurl_links: false` / `unfurl_media: false` when previews are undesirable.

## Key conclusion

We over-restricted Slack formatting if we treat Slack as only classic `mrkdwn`.

Better model:

1. **Normal assistant replies / first-class message tool**
   - Use Markdown-ish conversational text.
   - OpenClaw parses outbound Markdown into an intermediate representation and renders Slack-appropriate output.
   - Good for everyday replies, lightweight styling, links, bullets, code blocks, and buttons via `MessagePresentation` or Slack directives.

2. **OpenClaw `MessagePresentation`**
   - Good for portable cards, buttons, selects, dividers, and simple structured UI.
   - Works in Slack DMs.
   - Select warning icon needs follow-up before declaring selects polished.

3. **Raw Slack/plugin/channel-renderer work**
   - Slack supports richer Block Kit than our prior procedure implied:
     - `markdown` block
     - `rich_text` block
     - `table` block generated from markdown block
     - task/check lists
     - headers
     - fenced language code blocks
   - This should be documented as available for Slack-specific renderer/plugin work, not necessarily for every normal assistant reply.

## Recommended doc changes

Update `knowledge/procedures/platform-message-formatting.md` Slack section to distinguish:

- **Everyday assistant replies:** safe Markdown-ish text through OpenClaw.
- **Classic Slack `mrkdwn`:** still relevant for `section` text objects and many Block Kit fields.
- **Slack `markdown` block:** newer richer block that supports real Markdown features including headers, tables, task lists, nested formatting, and syntax-highlighted code blocks.
- **Slack `rich_text` block:** valid and powerful, especially for renderer/plugin output, but verbose to hand-author.
- **Tables:** avoid in plain chat text for portability, but do not claim Slack cannot render tables. Raw Slack markdown blocks can render real tables.
- **Unfurls:** set unfurl controls when testing or when docs previews are unwanted.

## Follow-up tests

- Quote-only rendering in normal OpenClaw path vs raw `mrkdwn` section vs raw `markdown` block.
- `MessagePresentation` select callback behavior and warning triangle root cause.
- `unfurl_links: false` / `unfurl_media: false` behavior through first-class message tool and raw Slack API.
- Whether first-class `message` tool can expose raw Slack `markdown` blocks cleanly, or whether this stays plugin-renderer-only.
