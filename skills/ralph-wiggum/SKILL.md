---
name: ralph-wiggum
description: Lightweight Ralph Wiggum loop workflow for small projects and tiny prototypes. Use when the user asks to "ralph", "Ralph Wiggum", "loop on this", "keep iterating until it works", build a small project, polish a toy app/script/tool, or turn a short idea into a shippable local artifact with repeated implementation + verification cycles. Not for large refactors, sensitive external actions, or projects needing more than a small bounded loop.
---

# Ralph Wiggum

Use a small, bounded version of the Ralph Wiggum technique: persistent iteration with real verification, not vibes. Ralph is basically: **do one small thing, check it, learn, repeat**.

## Fit Check

Use this skill when all are true:
- The project is small enough to finish or materially advance in 1–6 iterations.
- Verification is available: tests, lint, build, CLI output, screenshot, direct inspection, or a clear checklist.
- The work can be scoped to one local repo/project folder.

Do **not** use Ralph when:
- The task needs broad architecture, multi-day planning, or many files. Dispatch a heavier coding agent instead.
- It requires destructive actions, public posting, payment, credential changes, or external side effects without explicit confirmation.
- There is no meaningful completion check. Ask for success criteria first.

## Default Loop

1. **State the target** in one sentence.
2. **Create or update a tiny control file** in the project root unless the user objects:
   - `RALPH.md` for goal, constraints, checks, and current status.
   - `RALPH_LOG.md` for iteration notes if the project will take more than one pass.
3. **Pick one smallest next slice**. Avoid parallel feature soup.
4. **Implement the slice**.
5. **Run the smallest meaningful verification**.
6. **Record result**: pass/fail, evidence, next slice.
7. **Stop when done**, blocked, or safety/iteration limits are hit.

## Optional: Pair with Claude Foreman

Ralph can control the loop while Claude Foreman executes a heavy slice.

- Ralph owns the goal, state, iteration limit, and verification.
- Foreman may execute one slice when the slice is too large for comfortable inline work: multi-file edits, broad repo search, heavy test/build analysis, or code surgery that risks main-context sprawl.
- Present this as an option only when it helps. One line is enough: “This slice is chunky; I can dispatch it through Foreman and keep Ralph as the verifier.”
- Default stays inline. Foreman is the exception, not an automatic upgrade path.
- Record dispatched slices in `RALPH_LOG.md` with a `[foreman]` tag plus the profile used and verification result.

## Limits

Default limits unless user specifies otherwise:
- Max iterations: 6
- Max continuous runtime: 30 minutes
- Max scope: one small app/script/prototype or one narrowly-scoped repo improvement
- Commit only if the user asked for commits or the repo convention clearly expects it

If an iteration fails twice for the same reason, stop and reassess instead of thrashing. Ralph is persistent, not stupid. Very on-brand.

## RALPH.md Template

```markdown
# RALPH

## Goal
- <one-sentence target>

## Done Means
- [ ] <observable success condition>
- [ ] <test/build/manual check>

## Constraints
- Keep it small.
- Prefer boring dependencies.
- Do not expand scope without asking.

## Checks
- `<command or manual check>`

## Current Slice
- <small next task>

## Status
- Iteration: 0/<max>
- State: active | blocked | done
- Blocker: none
```

## Iteration Note Template

Append to `RALPH_LOG.md` after each pass:

```markdown
## Iteration <n> — <timestamp>

### Slice
- <what changed>

### Verification
- Command/check: `<...>`
- Result: pass | fail | blocked
- Evidence: <short output/screenshot/path>

### Learnings
- <what Ralph should remember next loop>

### Next
- <next smallest slice or DONE>
```

## Verification Bias

Prefer checks in this order:
1. Existing test command from README/package scripts/project docs
2. Typecheck/lint/build
3. Focused smoke command
4. Direct file inspection
5. Screenshot/manual UI check

Never claim completion without evidence. If no gate can run, say exactly why and mark it as a manual-check gap.

## Output Style

When reporting to the user, keep it short and include the run results:
- What changed
- Iterations run: `<completed>/<max>` plus final state (`done`, `blocked`, or `stopped at limit`)
- Verification evidence, including the final command/check and result
- What remains, if anything

If multiple iterations ran, summarize them in one compact line, e.g. `Iterations: 3/6 — pass, fail→fix, pass`. Avoid dumping the whole loop log unless asked.
