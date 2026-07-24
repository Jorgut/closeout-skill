# closeout (净化)

`closeout` is an evidence-driven, cross-platform Agent Skill for project knowledge reconciliation. It aligns code, runtime behavior, documentation, agent rules, authorized memory, and workspace residue, then reports exactly what was verified, changed, left pending, or held for approval.

Supported platforms include Codex, OpenCode, and Claude Code.

> [!IMPORTANT]
> Copying the `closeout/` folder installs the skill but does **not** register `/closeout`. Use the installer with `--commands` to add command adapters on platforms that support Markdown slash commands.

## Install

Requirements: Git and Python 3.10 or newer.

```bash
git clone https://github.com/Jorgut/closeout-skill.git
cd closeout-skill
```

Preview every destination and link without changing the machine:

```bash
python3 scripts/install_closeout.py --all-platforms --commands
```

After reviewing the plan, install explicitly:

```bash
python3 scripts/install_closeout.py \
  --all-platforms \
  --commands \
  --apply \
  --confirm
```

Restart the selected Agent applications after installation.

To install only selected platforms, repeat `--platform`:

```bash
python3 scripts/install_closeout.py \
  --platform codex \
  --platform opencode \
  --commands
```

## Platform Behavior

| Platform | Skill path | Command adapter | Invocation |
| --- | --- | --- | --- |
| Codex | `~/.codex/skills/closeout` | Not applicable | `$closeout` or natural language |
| OpenCode | `~/.config/opencode/skills/closeout` | `~/.config/opencode/commands/closeout.md` | `/closeout` |
| Claude Code | `~/.claude/skills/closeout` | `~/.claude/commands/closeout.md` | `/closeout` |

The installer keeps one canonical copy at `~/.agents/skills/closeout` and links each selected platform to it. This avoids maintaining separate copies while preserving each platform's expected discovery path.

Codex does not load the bundled Markdown slash-command adapter. Invoke the skill as `$closeout` or with natural language such as `Use closeout to reconcile this project's docs and agent rules.`

## Safety

- Installation is a dry run unless both `--apply` and `--confirm` are present.
- Every conflict is detected before any copy or link is created.
- Existing paths are never overwritten.
- A failed installation removes newly created links and its fresh canonical copy.
- Repeating the same installation is idempotent and reports `already-installed`.
- The closeout workflow never silently performs destructive cleanup.
- Cross-project writes and unauthorized memory changes require explicit approval.

## What closeout Covers

- Four modes: documentation sync, knowledge closeout, release closeout, and explicit workspace audit.
- Six fact planes: code, runtime, docs, rules, memory, and workspace.
- Evidence ledger: claim, source of truth, stale surface, action, verification, and final status.
- Project-adaptive verification for web apps, APIs, packages, desktop apps, Agent Skills, and documentation.
- Cleanup preview and final informed confirmation before destructive actions.
- Structured evals for trigger boundaries, permissions, behavior, and regressions.

Generic file organization, prose cleanup, data cleanup, and ordinary coding remain outside the trigger scope.

## Usage

```text
/closeout
/closeout reconcile the README and agent rules, but do not touch memory
$closeout verify this project's documentation against the implementation
净化一下，检查文档、规则文件和已授权记忆是否一致
```

See [`closeout/INSTALL.md`](closeout/INSTALL.md) for manual installation and smoke-test details. The full workflow and permission contract live in [`closeout/SKILL.md`](closeout/SKILL.md).

## Development

```bash
python3 -m unittest discover -s tests -v
python3 closeout/scripts/run_evals.py validate
python3 closeout/scripts/audit_inventory.py --project . --format markdown
```

### Eval-driven iteration

The eval suite is versioned at `closeout/evals/evals.json`. Each case declares whether the skill should trigger, required and forbidden output phrases, and forbidden action prefixes.

To grade results captured from fresh Agent sessions:

```bash
python3 closeout/scripts/run_evals.py grade --results /path/to/results.json
```

Every real failure should be reduced to a new regression case before its fix is released. Critical permission boundaries should pass three independent forward-test trials.

See [`closeout/references/evaluation.md`](closeout/references/evaluation.md) for the complete result schema and maintenance workflow.

## Acknowledgements

Closeout 2.0's governance and verification methodology was informed by and adapted from Neat Freak v3 by 数字生命卡兹克 under the MIT License. See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

Current release: `2.0.0-beta`.
