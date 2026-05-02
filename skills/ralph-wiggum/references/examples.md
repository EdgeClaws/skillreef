# Ralph Wiggum Examples

Load this only when you need a concrete pattern for starting a small Ralph project.

## Tiny Web Prototype

User: "Ralph a tiny landing page for the support insights idea."

Approach:
1. Create `RALPH.md` with visible done criteria: page loads, headline + CTA present, no console/build errors.
2. Inspect stack: `package.json`, README, existing app structure.
3. Implement one screen only.
4. Run `npm run build` or nearest equivalent.
5. If build fails, fix the smallest failure and rerun.
6. Report artifact path and build result.

## Script / CLI Tool

User: "Use Ralph to make a script that summarizes CSV rows."

Approach:
1. Define input/output examples before coding.
2. Create one script with no heavy dependencies unless clearly helpful.
3. Add a tiny fixture or inline sample.
4. Run the script against sample input.
5. Record command output in `RALPH_LOG.md`.

## Repo Polish Pass

User: "Ralph this README until the quickstart actually works."

Approach:
1. Treat README commands as the verification contract.
2. Run the quickstart exactly as written.
3. Patch only the first breakage found.
4. Rerun from a clean-ish state when feasible.
5. Stop after passing quickstart or after two same-cause failures.

## Ralph + Claude Foreman

User: "Ralph this small watchdog tool until the smoke test passes."

Approach:
1. Ralph creates `RALPH.md` with the smoke test as the done condition.
2. First slices stay inline: inspect README, run the smoke test, identify the first failure.
3. If a slice becomes chunky, offer Foreman: “This fix spans several files; I can dispatch this slice via Foreman and keep Ralph as verifier.”
4. Dispatch only that slice, then record `[foreman] profile=<profile>` in `RALPH_LOG.md`.
5. Ralph runs the verification check and decides the next slice.
6. Stop when the smoke test passes, the loop hits limits, or the same failure repeats twice.

## Bad Fits

- "Ralph our whole mobile app migration" → too broad; use a coding agent / larger plan.
- "Ralph this production deployment" → needs explicit approval and operational safeguards.
- "Ralph until you figure it out" with no success signal → ask for done criteria first.
