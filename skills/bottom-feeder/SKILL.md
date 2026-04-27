---
name: bottom-feeder
description: Depth-first knowledge crawling workflow that selects 1-2 high-value topics, researches with configured sources, synthesizes durable notes, and writes/updates files in knowledge/topics and knowledge/research. Use when asked to build or refresh knowledge files, run a scheduled knowledge-crawl, detect knowledge gaps, or run budget-aware research passes (supports any provider — Anthropic, OpenAI, Venice/Diem, etc.).
---

# Bottom Feeder

Run a modular 4-stage pipeline:
1) topic selection
2) research collection
3) synthesis
4) output writing

Prioritize depth over breadth. Default to 1 topic (max 2).

## Inputs to Load First

1. `config/defaults.yaml`
2. `config/topics.md`
3. If present, `config/next-topic.md` (force-priority override)
4. If present, `config/run-policy.md` (hard run constraints; treat as mandatory for this run)

## Workflow

### 1) Select topic

Use these modules in order:
- `references/topic-selection/hardcoded-list.md`
- `references/topic-selection/conversation-mining.md`
- `references/topic-selection/knowledge-gaps.md`
- `references/topic-selection/knowledge-refresh.md`
- `references/topic-selection/trending.md`

Combine candidates, dedupe, score, and pick top 1-2.

Before finalizing topic, run a quick duplicate check:
- Search `knowledge/` for existing coverage.
- If coverage is already strong and recent, skip and pick next candidate.

### 2) Collect research

Pick sources by topic type using:
- `references/research-sources/brave.md` (baseline)
- `references/research-sources/perplexity.md` (optional deep synth)
- `references/research-sources/twitter.md` (optional sentiment/news pulse)
- `references/research-sources/coingecko.md` (optional crypto data)
- `references/research-sources/coinmarketcap.md` (optional crypto metadata)
- `references/research-sources/browser.md` (optional page extraction)

Low-cost default: brave only, plus local knowledge lookup.

### 3) Synthesize

Create one durable, standalone knowledge artifact per topic:
- What it is
- Current state
- Why it matters (for the user's ecosystem/team/work)
- Key entities/projects
- Open questions + what to watch
- Sources with dates

For updates, include a short "What's new since last update" section.

### 3.5) Quality gate

Before advancing to the next topic, run:
- `references/quality-gate/completion-checklist.md`

Every section must pass or be explicitly tagged `[INCOMPLETE: reason]`.
Do not start topic N+1 until topic N clears the gate.

### 4) Write output

Use:
- `references/output/knowledge-writer.md`
- `references/output/run-progress.md`
- `references/output/lobsearch-index.md`

Write immediately after each topic (incremental write, never batch all topics first).

After writing each topic, update the run progress log (`knowledge/.runs/<date>-<mode>.md`).
This is your audit trail — always current, even if the run is interrupted.

## Modes

### Routine mode (default)
- 1 topic
- low-cost sources
- concise synthesis
- quiet completion unless user asked for report

### Burn mode (explicit only)
Use when user explicitly asks to consume remaining credits/budget aggressively.

Steps:
1. Run `scripts/provider-usage.sh` to check current usage (supports Tide Pools, legacy lobster, or generic `openclaw status` fallback)
2. Run `scripts/check-balance.sh` if you have balance JSON input to parse (supports generic fields: `remaining`, `balance`, `credits`, or Venice-specific `venice.data.diem`)
3. Keep reserve from config: use `min_reserve_usd` when set (>0), otherwise fall back to legacy `min_reserve_diem`
4. Use heavier model + more sources (all optional sources enabled)
5. Save after every topic (incremental write — never batch)
6. Stop gracefully if balance or provider limit is hit
7. If multiple auth profiles are available, monitor for exhaustion and note when rotation is needed

### Provider lock (when configured)
If `config/run-policy.md` specifies a `provider_lock`, enforce it strictly:
- Do not use non-locked providers/models for synthesis.
- If the locked provider is unavailable, paused, or rate-limited, stop and ask user whether to wait or change policy.
- Record provider compliance in the run progress file (`knowledge/.runs/...`).

## Ad-hoc topic injection

Users can pass topics directly instead of using the seed list:
- "Run bottom feeder on [topic1, topic2, ...]"
- Ad-hoc topics skip the selection stage entirely — go straight to research.
- Still subject to quality gate and progress logging.

## Guardrails

- Never spend down to zero unless user explicitly says to.
- Avoid duplicate rewrites when no meaningful updates exist.
- Prefer free/local sources first.
- If source collection is weak, write a partial with clear uncertainty notes.
- Keep files readable; split oversized output into follow-up research files.
- In burn mode with multiple auth profiles, track which profile is active and flag when switching is needed.

## Quick manual run recipe

1. Pick one topic from `config/topics.md`
2. Run brave search (3-6 results)
3. Synthesize into `knowledge/topics/<slug>.md`
4. Log run note in `memory/daily/YYYY-MM-DD.md`
5. Report: topic, files changed, estimated cost mode used
