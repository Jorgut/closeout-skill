#!/usr/bin/env python3
"""Safely install closeout across supported agent platforms."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any


SKILL_NAME = "closeout"
PLATFORMS = ("codex", "opencode", "claude")


class InstallError(RuntimeError):
    """Raised when installation would overwrite an existing path."""


def platform_paths(home: Path) -> dict[str, dict[str, Path | None]]:
    return {
        "codex": {
            "skill": home / ".codex/skills" / SKILL_NAME,
            "command": None,
        },
        "opencode": {
            "skill": home / ".config/opencode/skills" / SKILL_NAME,
            "command": home / ".config/opencode/commands" / f"{SKILL_NAME}.md",
        },
        "claude": {
            "skill": home / ".claude/skills" / SKILL_NAME,
            "command": home / ".claude/commands" / f"{SKILL_NAME}.md",
        },
    }


def existing_status(path: Path, target: Path) -> str:
    if not path.exists() and not path.is_symlink():
        return "create"
    try:
        return "unchanged" if path.resolve() == target.resolve() else "conflict"
    except OSError:
        return "conflict"


def directory_digest(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if not item.is_file() or item.is_symlink():
            continue
        relative = item.relative_to(path).as_posix().encode()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(item.read_bytes())
    return digest.hexdigest()


def canonical_status(source: Path, canonical: Path) -> str:
    if not canonical.exists() and not canonical.is_symlink():
        return "copy"
    try:
        if canonical.resolve() == source.resolve():
            return "unchanged"
        if not (canonical / "SKILL.md").is_file():
            return "conflict"
        return "unchanged" if directory_digest(canonical) == directory_digest(source) else "conflict"
    except OSError:
        return "conflict"


def validate_source(source: Path, commands: bool) -> None:
    if not (source / "SKILL.md").is_file():
        raise InstallError(f"missing SKILL.md: {source}")
    command = source / "commands" / f"{SKILL_NAME}.md"
    if commands and not command.is_file():
        raise InstallError(f"missing command adapter: {command}")


def build_plan(source: Path, home: Path, platforms: list[str], commands: bool) -> dict[str, Any]:
    source = source.expanduser().resolve()
    home = home.expanduser().resolve()
    validate_source(source, commands)
    canonical = home / ".agents/skills" / SKILL_NAME
    operations: list[dict[str, str]] = [
        {
            "kind": "canonical-skill",
            "path": str(canonical),
            "target": str(source),
            "status": canonical_status(source, canonical),
        }
    ]
    paths = platform_paths(home)
    for platform in platforms:
        skill_path = paths[platform]["skill"]
        assert skill_path is not None
        operations.append(
            {
                "kind": f"{platform}-skill-link",
                "path": str(skill_path),
                "target": str(canonical),
                "status": existing_status(skill_path, canonical),
            }
        )
        command_path = paths[platform]["command"]
        if commands and command_path is not None:
            canonical_command = canonical / "commands" / f"{SKILL_NAME}.md"
            operations.append(
                {
                    "kind": f"{platform}-command-link",
                    "path": str(command_path),
                    "target": str(canonical_command),
                    "status": existing_status(command_path, canonical_command),
                }
            )
    conflicts = [operation for operation in operations if operation["status"] == "conflict"]
    return {
        "action": "install",
        "status": "conflict" if conflicts else "ready",
        "read_only": True,
        "source": str(source),
        "canonical_path": str(canonical),
        "platforms": platforms,
        "commands_requested": commands,
        "operations": operations,
        "conflicts": conflicts,
        "codex_invocation": "$closeout",
        "slash_commands": ["/closeout"]
        if commands and any(paths[platform]["command"] is not None for platform in platforms)
        else [],
    }


def copy_canonical(source: Path, canonical: Path) -> None:
    canonical.parent.mkdir(parents=True, exist_ok=True)
    staged = Path(tempfile.mkdtemp(prefix=".closeout-install-", dir=canonical.parent))
    try:
        staged.rmdir()
        shutil.copytree(source, staged, symlinks=False)
        staged.rename(canonical)
    except Exception:
        if staged.exists():
            shutil.rmtree(staged)
        raise


def apply_plan(plan: dict[str, Any]) -> dict[str, Any]:
    if plan["conflicts"]:
        paths = ", ".join(item["path"] for item in plan["conflicts"])
        raise InstallError(f"existing paths would be overwritten: {paths}")

    canonical = Path(plan["canonical_path"])
    created_links: list[Path] = []
    canonical_created = False
    try:
        if plan["operations"][0]["status"] == "copy":
            copy_canonical(Path(plan["source"]), canonical)
            canonical_created = True
        for operation in plan["operations"][1:]:
            if operation["status"] != "create":
                continue
            path = Path(operation["path"])
            target = Path(operation["target"])
            path.parent.mkdir(parents=True, exist_ok=True)
            path.symlink_to(target, target_is_directory=operation["kind"].endswith("skill-link"))
            created_links.append(path)
    except Exception:
        for path in reversed(created_links):
            path.unlink(missing_ok=True)
        if canonical_created and canonical.exists():
            shutil.rmtree(canonical)
        raise

    result = dict(plan)
    result["read_only"] = False
    result["status"] = "already-installed" if not canonical_created and not created_links else "installed"
    result["created"] = ([str(canonical)] if canonical_created else []) + [
        str(path) for path in created_links
    ]
    return result


def emit_markdown(result: dict[str, Any]) -> None:
    print("# closeout Install")
    print()
    print(f"- status: {result['status']}")
    print(f"- mode: {'preview' if result['read_only'] else 'apply'}")
    print(f"- canonical: `{result['canonical_path']}`")
    print(f"- platforms: {', '.join(result['platforms'])}")
    print(f"- command adapters: {str(result['commands_requested']).lower()}")
    print()
    for operation in result["operations"]:
        print(f"- {operation['status']}: `{operation['path']}`")
        print(f"  - target: `{operation['target']}`")
    if result["conflicts"]:
        print("\nInstallation refused: existing paths would be overwritten.")
    elif result["read_only"]:
        print("\nNo files or links changed. Re-run with --apply --confirm after review.")
    else:
        print("\nRestart installed Agent applications before using the new command.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install closeout across agent platforms.")
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--all-platforms", action="store_true")
    selection.add_argument("--platform", action="append", choices=PLATFORMS, default=[])
    parser.add_argument("--commands", action="store_true")
    parser.add_argument("--source", default=str(Path(__file__).resolve().parent.parent / "closeout"))
    parser.add_argument("--home", default=str(Path.home()))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm", action="store_true")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    platforms = list(PLATFORMS) if args.all_platforms else list(dict.fromkeys(args.platform))
    try:
        plan = build_plan(Path(args.source), Path(args.home), platforms, args.commands)
        if args.apply != args.confirm:
            raise InstallError("installation requires both --apply and --confirm")
        result = apply_plan(plan) if args.apply else plan
    except (OSError, InstallError) as exc:
        if args.format == "json":
            print(json.dumps({"action": "install", "status": "refused", "error": str(exc)}, indent=2))
        else:
            print(f"Installation refused: {exc}")
        raise SystemExit(2) from None
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        emit_markdown(result)


if __name__ == "__main__":
    main()
