# closeout (净化)

`closeout` is a cross-platform Agent Skill for end-of-session knowledge reconciliation. It checks project documentation, agent rule files, and authorized memory against the current implementation, applies only safe reversible fixes, and reports destructive or cross-project changes for explicit approval.

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

- Reconcile README and project documentation with current code and configuration.
- Reconcile `CLAUDE.md`, `AGENTS.md`, and platform-equivalent rule files.
- Verify authorized agent memory and report unknown memory systems as read-only.
- Identify stale plans, debug artifacts, and superseded files as deletion candidates.
- Produce a closeout report with impact, changed files, decisions needed, and residual risk.

It intentionally excludes branch cleanup, worktree deletion, deployment verification, release automation, and generic file or prose tidying.

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
```

Current release: `1.1.0-beta`.
