---
name: web-extract
description: "Choose and use the right web extraction path for a task. Use when pulling data from websites, especially when deciding between lightweight retrieval, protected-site extraction, Amazon-specific APIs, programmable browser backends, or interactive browsing. Good triggers: Cloudflare/bot-blocked pages, CamelCamelCamel/price-history lookup, 'scrape this page', 'extract structured data from this site', 'find a dependable backend', or when another skill like shop-agent needs site data but should stay backend-agnostic."
---

# Web Extract

Route web-data tasks to the lightest dependable backend. Keep domain skills, like shopping, separate from extraction strategy.

## Routing rules

1. Start with the lightest viable path.
2. Escalate only when the simpler path will clearly fail or already failed.
3. Treat paid/API-credit backends as deliberate choices, not defaults.
4. Keep interactive human-visible browsing separate from server-side extraction.

## Backend selection order

### 1) Lightweight retrieval
Use built-in lightweight tools first when they are enough:
- `web_search` for discovery and quick source finding
- `browser` for simple page inspection or human-visible interaction
- direct site reads only when the page is easy and unprotected

Choose this path for:
- quick fact lookup
- finding candidate URLs
- reading public pages that do not need structured extraction

### 2) Browserless
Use Browserless as the default backend for **protected server-side extraction**.

Choose it for:
- Cloudflare or anti-bot friction
- CamelCamelCamel or similar protected pages
- extracting data from a hard page without needing a human-visible browser
- cases where `/stealth/bql` or `/unblock` fits better than a naive headless fetch

Read `references/backends.md` for credentials and positioning.

### 3) TinyFish
Use TinyFish when you need a **remote stealth browser primitive**, especially for brittle or multi-step flows.

Choose it for:
- hard pages where a full remote browser session is useful
- CDP / Playwright-style control on a hosted browser
- cases where the higher-level agent flow is too fuzzy but the site still needs stealthy browser execution

Important nuance: for CCC-style protected extraction, do **not** assume the TinyFish Agent API is the right first surface. The better current fit is the TinyFish Browser API / CDP session.

Read `references/backends.md` for credentials and positioning.

### 4) Rainforest API
Use Rainforest only for **Amazon-native structured data**, and only when:
- the user explicitly asks for it, or
- you recommend it first and the tradeoff is worth spending a credit

Do **not** treat Rainforest as the default web-extraction path.

Good fits:
- structured Amazon search results
- ASIN/product detail lookup
- fresh price confirmation before checkout

Bad fits:
- true historical price data
- general-purpose scraping
- casual browsing when a free/manual path is good enough

Read `references/backends.md` and `references/shopping.md`.

### 5) Interactive browser mode
Use the OpenClaw `browser` tool when the task truly needs a person-facing session:
- login
- 2FA
- CAPTCHA/manual solve
- visual confirmation
- final shopping steps

## Escalation patterns

### Protected page extraction
1. Try Browserless first, especially `/stealth/bql` or `/unblock`.
2. If you need deeper remote browser control, try TinyFish Browser API / CDP session.
3. If both fail and the user has a real browser path available, switch to interactive browser work.
4. If the site remains blocked, report the limitation plainly.

When doing repeatable operational work, prefer the bundled helpers before rewriting one-off curl/CDP glue:
- `scripts/browserless_extract.py`
- `scripts/tinyfish_browser_extract.py`

### Amazon shopping support
1. Prefer free/manual browsing for casual research.
2. Suggest Rainforest when structured Amazon data would materially help.
3. Spend Rainforest credits only on request or after proposing the tradeoff.
4. Use interactive browser flow for cart/login/checkout.

### CamelCamelCamel / price history
1. Do not use Rainforest for history, it does not solve that problem.
2. Try Browserless first for protected extraction.
3. Try TinyFish Browser API / CDP session if you need a second VPS-side lane.
4. If blocked, say so clearly and offer a manual/browser alternative.

## Reference files

- `references/backends.md` - backend roles, secret paths, and canonical policy
- `references/shopping.md` - how shopping-related tasks should use this skill

## Bundled helper scripts

- `scripts/browserless_extract.py` - normalized extraction helper for Browserless `content`, `unblock`, or `stealth-bql`
- `scripts/tinyfish_browser_extract.py` - create a TinyFish browser session, drive it over CDP, and return normalized extraction JSON
