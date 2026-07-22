# closeout (净化) — Install & Smoke Test

## Quick Install (Local)

```bash
# Option A: Symlink into your local skills directory
# OpenCode
ln -s /absolute/path/to/session-closeout-skill/closeout ~/.config/opencode/skills/closeout

# Claude Code
ln -s /absolute/path/to/session-closeout-skill/closeout ~/.claude/skills/closeout

# Codex
ln -s /absolute/path/to/session-closeout-skill/closeout ~/.codex/skills/closeout
```

```bash
# Option B: Copy (if you prefer isolation)
cp -r /path/to/session-closeout-skill/closeout ~/.config/opencode/skills/closeout
```

## Verify Install

```bash
# Should show closeout in skill list
# OpenCode
opencode skill list

# Or just check the directory exists
ls ~/.config/opencode/skills/closeout/
# Expected: SKILL.md  references/  evals/
```

## Smoke Test (run once after install)

1. **Open a project** that has some code, a README, and optionally a CLAUDE.md
2. **Make a small change** (e.g., update a version number, add a command to README)
3. **Trigger closeout**:
   ```
   /closeout
   ```
   or natural language:
   ```
   sync docs and memory
   净化一下
   ```
4. **Verify behavior**:
   - Skill inventories markdown + rule files
   - Compares against current code/config
   - Applies safe auto-fixes (e.g., missing `.env*` in `.gitignore`)
   - Lists any deletion candidates (throw-away plans, `*_old.*` files)
   - Produces two-phase report with **Impact**, **Changed/Created**, **Needs Your Decision**, **Residual**
5. **Confirm it did NOT**:
   - Delete branches/worktrees (out of scope)
   - Trigger on "tidy up this file" (excluded)
   - Write to memory without explicit authorization

## Expected Artifacts After Smoke Test

- Updated README/CLAUDE.md (if discrepancies existed)
- `references/verification-checklist.md` items all `pass` or `waived-with-reason`
- Report output in chat following the two-phase format

## Packaging for Public Distribution (later)

When ready to publish:
1. Ensure `closeout/` directory is the package root
2. Add a minimal `README.md` at package root (not in skill dir) with:
   - One-line description
   - Install command
   - Trigger examples
   - Link to this skill's repo
3. Tag version: `v1.0.0`
4. Publish to ClawHub / Tessl registry or your preferred skill registry

## Local Dev Notes

- The skill is **self-contained**: no external scripts, no `assets/`, no `scripts/` needed for v1
- All platform logic lives in `references/platform-behavior.md` (read-only guidance)
- `evals/evals.json` covers 3 trigger families + 3 negative boundaries
- Line budget: SKILL.md ≤ 500 lines (currently ~100)