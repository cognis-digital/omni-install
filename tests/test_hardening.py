"""
Hardening tests for omni-install.

Covers the error/edge-case paths added in the hardening pass:
  - omni.py: bad input, out-of-range selection, EOF on stdin, no package manager
  - integrations/webhook.py: bad URL, empty stdin, non-JSON stdin, malformed header
"""
from __future__ import annotations

import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REPO = Path(__file__).resolve().parent.parent
PYTHON = sys.executable

# ---------------------------------------------------------------------------
# omni.py tests
# ---------------------------------------------------------------------------

sys.path.insert(0, str(REPO))
import omni  # noqa: E402  (must come after sys.path tweak)


class TestOmniMgr(unittest.TestCase):
    def test_mgr_returns_string(self):
        """mgr() must always return a string (possibly empty)."""
        result = omni.mgr()
        self.assertIsInstance(result, str)

    def test_mgr_windows(self):
        with patch("platform.system", return_value="Windows"):
            self.assertEqual(omni.mgr(), "winget")

    def test_mgr_brew(self):
        with patch("platform.system", return_value="Linux"), \
             patch("shutil.which", side_effect=lambda n: "/usr/local/bin/brew" if n == "brew" else None):
            self.assertEqual(omni.mgr(), "brew")

    def test_mgr_no_manager(self):
        with patch("platform.system", return_value="Linux"), \
             patch("shutil.which", return_value=None):
            self.assertEqual(omni.mgr(), "")


class TestOmniInstall(unittest.TestCase):
    def test_install_unknown_tool_does_not_raise(self):
        """install() with an unknown tool name must print to stderr, not raise KeyError."""
        buf = io.StringIO()
        with patch("sys.stderr", buf):
            omni.install("__unknown_tool__", "apt")
        self.assertIn("unknown tool", buf.getvalue())

    def test_install_no_package_for_manager(self):
        """install() when there's no package for the chosen manager prints a message."""
        captured = io.StringIO()
        with patch("builtins.print", side_effect=lambda *a, **kw: captured.write(" ".join(str(x) for x in a) + "\n")):
            omni.install("Ollama", "brew")  # Ollama has no brew entry
        self.assertIn("no brew package", captured.getvalue())


class TestOmniMain(unittest.TestCase):
    def test_no_manager_returns_1(self):
        """main() returns 1 (and prints to stderr) when no package manager is found."""
        with patch("omni.mgr", return_value=""):
            result = omni.main()
        self.assertEqual(result, 1)

    def test_eof_on_input_returns_1(self):
        """main() must return 1 cleanly when stdin raises EOFError (piped empty input)."""
        with patch("omni.mgr", return_value="apt"), \
             patch("builtins.input", side_effect=EOFError):
            result = omni.main()
        self.assertEqual(result, 1)

    def test_keyboard_interrupt_returns_1(self):
        """main() must return 1 cleanly on KeyboardInterrupt (Ctrl-C)."""
        with patch("omni.mgr", return_value="apt"), \
             patch("builtins.input", side_effect=KeyboardInterrupt):
            result = omni.main()
        self.assertEqual(result, 1)

    def test_empty_selection_returns_1(self):
        """main() returns 1 when the user enters nothing meaningful."""
        with patch("omni.mgr", return_value="apt"), \
             patch("builtins.input", return_value=""):
            result = omni.main()
        self.assertEqual(result, 1)

    def test_out_of_range_selection_skipped(self):
        """Out-of-range indices are skipped; valid ones proceed."""
        calls = []
        with patch("omni.mgr", return_value="apt"), \
             patch("builtins.input", return_value="999"), \
             patch("omni.install", side_effect=lambda n, m: calls.append(n)):
            result = omni.main()
        # 999 is out of range -> nothing installed -> returns 1
        self.assertEqual(result, 1)
        self.assertEqual(calls, [])

    def test_valid_selection_calls_install(self):
        """A valid single-item selection calls install() exactly once."""
        calls = []
        with patch("omni.mgr", return_value="apt"), \
             patch("builtins.input", return_value="1"), \
             patch("omni.install", side_effect=lambda n, m: calls.append(n)):
            result = omni.main()
        self.assertEqual(result, 0)
        self.assertEqual(len(calls), 1)

    def test_select_all(self):
        """'a' selects all tools."""
        calls = []
        with patch("omni.mgr", return_value="apt"), \
             patch("builtins.input", return_value="a"), \
             patch("omni.install", side_effect=lambda n, m: calls.append(n)):
            result = omni.main()
        self.assertEqual(result, 0)
        self.assertEqual(len(calls), len(omni.CATALOG))


# ---------------------------------------------------------------------------
# integrations/webhook.py tests (run as subprocess so argparse works cleanly)
# ---------------------------------------------------------------------------

WEBHOOK = str(REPO / "integrations" / "webhook.py")


class TestWebhook(unittest.TestCase):
    def _run(self, args: list[str], stdin: str = "") -> subprocess.CompletedProcess:
        return subprocess.run(
            [PYTHON, WEBHOOK] + args,
            input=stdin,
            capture_output=True,
            text=True,
        )

    def test_bad_url_scheme_exits_2(self):
        """Non-http(s) URL must exit with code 2 and print an error."""
        proc = self._run(["--url", "ftp://example.com/hook"], stdin='{"k":"v"}')
        self.assertEqual(proc.returncode, 2)
        self.assertIn("http", proc.stderr)

    def test_empty_stdin_exits_2(self):
        """Empty stdin must exit with code 2."""
        proc = self._run(["--url", "https://example.com/hook"], stdin="   ")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("empty", proc.stderr)

    def test_non_json_stdin_exits_2(self):
        """Non-JSON stdin must exit with code 2."""
        proc = self._run(["--url", "https://example.com/hook"], stdin="not-json")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("JSON", proc.stderr)

    def test_malformed_header_warns(self):
        """A --header without ':' should warn but NOT crash (may still fail on network)."""
        proc = self._run(
            ["--url", "https://httpbin.org/post", "--header", "NoColonHere"],
            stdin=json.dumps({"x": 1}),
        )
        # The warning must appear; return code may be 0 or 1 depending on network
        self.assertIn("malformed", proc.stderr)

    def test_missing_url_arg_exits_nonzero(self):
        """Omitting --url must exit non-zero (argparse error)."""
        proc = self._run([])
        self.assertNotEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
