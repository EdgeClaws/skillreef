# Web Extract for Shopping Tasks

Use this file when `shop-agent` needs site data but should stay backend-agnostic.

## Shopping policy

### Casual product research
Prefer free/manual paths first:
- regular browsing
- direct retailer search
- lightweight web lookup

Do not spend Rainforest credits by default.

### Structured Amazon lookup
Suggest Rainforest when one of these is true:
- you need clean Amazon search results with ASINs
- you need a fresh product detail lookup before presenting a buy choice
- you need a final price confirmation before checkout

Before using Rainforest, either:
- get an explicit user request, or
- tell the user you can spend a credit for cleaner structured Amazon data

### Historical Amazon price context
Rainforest is not the answer.

For true history:
- prefer CamelCamelCamel or similar history sources
- if protected, try Browserless first, especially `stealth-bql` or `unblock`
- if you need a second VPS-side lane, try TinyFish Browser API / CDP session next
- if both fail, fall back to manual/browser-assisted checking

Current operational helpers live in:
- `scripts/browserless_extract.py`
- `scripts/tinyfish_browser_extract.py`

### Checkout and human steps
Use the OpenClaw `browser` tool, not TinyFish or Browserless, for:
- login
- 2FA
- payment review
- final order approval path

## Suggested phrasing

When Rainforest would help but is not required:
- "I can use a Rainforest credit to get cleaner Amazon results if you want."
- "I can probably do this manually for free, or spend a Rainforest credit for a cleaner structured lookup."

When history is blocked:
- "I can try the protected-page path, but this site may still block server-side extraction."
