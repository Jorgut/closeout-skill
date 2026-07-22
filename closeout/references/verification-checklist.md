# Verification Checklist Reference

## Mandatory Verification Items

Before declaring closeout complete, **every item below must be `pass` or `waived-with-reason`**.

### 1. Fact Plane Coverage
- [ ] Code plane: current implementation matches docs/rules (commands, config, schema, tests)
- [ ] Runtime plane: deploy marker / live service / real page/API verified (or `not-applicable`)
- [ ] Docs plane: README and `docs/` reflect current reality (no v1.0 claims on v3 code)
- [ ] Rules plane: CLAUDE.md / AGENTS.md constraints are current and executable
- [ ] Memory plane: authorized memory entries are accurate; stale entries condensed or removed
- [ ] Workspace plane: session residue identified; deletion candidates listed with reasons

### 2. Rule Enforcement Audit
- [ ] Naming conventions mechanically verified (e.g., kebab-case dirs)
- [ ] Required files exist (CLAUDE.md, AGENTS.md symlink, .gitignore with `.env*`)
- [ ] Symlink integrity: AGENTS.md → CLAUDE.md (or platform equivalent)
- [ ] Red lines enforced: `.gitignore` has `.env*`, no secrets in code
- [ ] Directory discipline: no loose files in project root
- [ ] No duplicate/parallel versions of the same fact across layers

### 3. Permission Boundary Compliance
- [ ] All auto-fixes were safe/reversible/purely-additive
- [ ] All report-first actions are documented in "Needs Your Decision" with both sides' evidence
- [ ] No silent destructive mutations occurred
- [ ] No cross-project writes without explicit confirmation
- [ ] Unknown memory platforms defaulted to read-only report

### 4. Reference Integrity
- [ ] Every path/command/project referenced in rule files exists in reality
- [ ] Dead references cleaned or reported
- [ ] CLAUDE.md / AGENTS.md symlink intact and not diverged

### 5. Closeout Report Quality
- [ ] Two-phase report format used (pre-cleanup → post-cleanup after confirmation)
- [ ] Impact statement explains what misalignment/risk/handoff-cost was eliminated
- [ ] Changed/Created list is specific (file + what + why)
- [ ] Deletion candidates have reasons; none deleted without confirmation
- [ ] Residual section explicitly lists pending/out-of-scope/warnings (or "None")
- [ ] No "guaranteed clean" language masking pending items

### 6. Platform-Specific Gates
- [ ] OpenCode: memory size within soft budget; no orphaned memory files
- [ ] Claude Code: no manual memory writes (platform manages consolidation)
- [ ] Codex: AGENTS.md ≤ 25 KB; memories/ not hand-edited
- [ ] Unknown platform: memory section explicitly marked `generated-read-only` or `unknown-fallback`

### 7. Scope Discipline
- [ ] Workspace cleanup (branches, worktrees, temp files) NOT performed unless explicitly requested AND confirmed
- [ ] Release/deploy closeout (PR, CI, prod, CDN) NOT performed unless Full Path triggered
- [ ] Generic tidying / prose cleanup / data reorganization NOT performed

## Waiver Format

If any item cannot be `pass`, it must be `waived-with-reason`:
```
- [ ] Item N: WAIVED — <specific reason, e.g., "no deploy exists in this project", "platform memory API unavailable">
```

## Failure Policy

If any mandatory item is neither `pass` nor `waived-with-reason`:
- Closeout is **incomplete**
- Report must list failing items under **Residual** with `pending` status
- User must decide whether to proceed, investigate, or abort