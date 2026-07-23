from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import install_closeout  # noqa: E402


class InstallCloseoutTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        root = Path(self.temporary.name)
        self.source = root / "closeout"
        self.home = root / "home"
        (self.source / "commands").mkdir(parents=True)
        (self.source / "SKILL.md").write_text(
            "---\nname: closeout\ndescription: Test closeout\n---\n",
            encoding="utf-8",
        )
        (self.source / "commands/closeout.md").write_text(
            "---\ndescription: Test command\n---\nUse closeout.\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_preview_does_not_write(self) -> None:
        result = install_closeout.build_plan(
            self.source, self.home, list(install_closeout.PLATFORMS), True
        )

        self.assertEqual(result["status"], "ready")
        self.assertTrue(result["read_only"])
        self.assertFalse(self.home.exists())

    def test_apply_is_idempotent(self) -> None:
        plan = install_closeout.build_plan(
            self.source, self.home, list(install_closeout.PLATFORMS), True
        )
        result = install_closeout.apply_plan(plan)

        self.assertEqual(result["status"], "installed")
        self.assertEqual(result["slash_commands"], ["/closeout"])
        canonical = self.home / ".agents/skills/closeout"
        self.assertTrue((canonical / "SKILL.md").is_file())
        for path in [
            self.home / ".codex/skills/closeout",
            self.home / ".config/opencode/skills/closeout",
            self.home / ".claude/skills/closeout",
            self.home / ".config/opencode/commands/closeout.md",
            self.home / ".claude/commands/closeout.md",
        ]:
            self.assertTrue(path.is_symlink())
        self.assertFalse((self.home / ".codex/commands/closeout.md").exists())

        repeated_plan = install_closeout.build_plan(
            self.source, self.home, list(install_closeout.PLATFORMS), True
        )
        repeated = install_closeout.apply_plan(repeated_plan)
        self.assertEqual(repeated["status"], "already-installed")
        self.assertEqual(repeated["created"], [])

    def test_conflict_refuses_before_writing(self) -> None:
        conflict = self.home / ".claude/commands/closeout.md"
        conflict.parent.mkdir(parents=True)
        conflict.write_text("keep me", encoding="utf-8")
        plan = install_closeout.build_plan(
            self.source, self.home, list(install_closeout.PLATFORMS), True
        )

        with self.assertRaises(install_closeout.InstallError):
            install_closeout.apply_plan(plan)

        self.assertEqual(conflict.read_text(encoding="utf-8"), "keep me")
        self.assertFalse((self.home / ".agents/skills/closeout").exists())

    def test_mismatched_canonical_copy_is_a_conflict(self) -> None:
        canonical = self.home / ".agents/skills/closeout"
        canonical.mkdir(parents=True)
        (canonical / "SKILL.md").write_text("different", encoding="utf-8")

        plan = install_closeout.build_plan(
            self.source, self.home, ["codex"], False
        )

        self.assertEqual(plan["status"], "conflict")
        self.assertEqual(
            Path(plan["conflicts"][0]["path"]).resolve(), canonical.resolve()
        )


if __name__ == "__main__":
    unittest.main()
