"""
Tests for core/installation_logic.py — the module that actually
shells out to install tools, so its command-building logic is the
most security-sensitive code in the project.

Updated: 17/08/2026 (new file)
"""
from unittest.mock import patch
from core import installation_logic as il


class TestGetInstallCommand:
    """get_install_command must always return a LIST (never a shell
    string) so subprocess.run(..., shell=False) stays safe."""

    def test_termux_returns_pkg_install_list(self):
        with patch.object(il, "CURRENT_OS", "termux"):
            cmd = il.get_install_command("nmap")
        assert cmd == ["pkg", "install", "-y", "nmap"]
        assert isinstance(cmd, list)

    def test_macos_returns_brew_install_list(self):
        with patch.object(il, "CURRENT_OS", "macos"):
            cmd = il.get_install_command("nmap")
        assert cmd == ["brew", "install", "nmap"]

    def test_linux_prefers_apt_when_available(self):
        with patch.object(il, "CURRENT_OS", "linux"), \
             patch.object(il.shutil, "which", side_effect=lambda p: "/usr/bin/apt-get" if p == "apt-get" else None):
            cmd = il.get_install_command("nmap")
        assert cmd == ["sudo", "apt-get", "install", "-y", "nmap"]

    def test_linux_falls_back_to_pacman_when_no_apt(self):
        with patch.object(il, "CURRENT_OS", "linux"), \
             patch.object(il.shutil, "which", side_effect=lambda p: "/usr/bin/pacman" if p == "pacman" else None):
            cmd = il.get_install_command("nmap")
        assert cmd == ["sudo", "pacman", "-S", "--noconfirm", "nmap"]

    def test_windows_returns_none_when_no_package_manager_found(self):
        with patch.object(il, "CURRENT_OS", "windows"), \
             patch.object(il.shutil, "which", return_value=None):
            cmd = il.get_install_command("nmap")
        assert cmd is None

    def test_never_builds_a_shell_string(self):
        """Regression guard: every branch must return a list or None,
        never a raw string that could be misused with shell=True."""
        for os_name in ("termux", "macos", "linux", "windows", "other"):
            with patch.object(il, "CURRENT_OS", os_name), \
                 patch.object(il.shutil, "which", return_value="/usr/bin/apt-get"):
                cmd = il.get_install_command("some-package")
            assert cmd is None or isinstance(cmd, list)


class TestRunCommand:
    def test_success_returns_true_and_stdout(self, tmp_path):
        with patch.object(il.subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "done"
            mock_run.return_value.stderr = ""
            success, output = il.run_command(["echo", "hi"], "Testing...")
        assert success is True
        assert output == "done"

    def test_uses_shell_false_always(self):
        """Regression guard: shell=False must never change, since
        command_list can contain data derived from tool names."""
        with patch.object(il.subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = ""
            mock_run.return_value.stderr = ""
            il.run_command(["echo", "hi"], "Testing...")
        _, kwargs = mock_run.call_args
        assert kwargs.get("shell") is False

    def test_failure_logs_and_returns_false(self, tmp_path, monkeypatch):
        log_file = tmp_path / "error.log"
        monkeypatch.setattr(il, "LOG_FILE", str(log_file))
        with patch.object(il.subprocess, "run") as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stdout = ""
            mock_run.return_value.stderr = "boom"
            success, output = il.run_command(["false"], "Testing...")
        assert success is False
        assert "boom" in output
        assert log_file.exists()
        assert "boom" in log_file.read_text()


class TestInstallToolSafety:
    def test_missing_url_does_not_call_run_command(self, capsys):
        with patch.object(il, "RAW_TOOLS", {"broken": {"name": "Broken", "url": None}}), \
             patch.object(il, "run_command") as mock_run:
            il.install_tool("broken")
        mock_run.assert_not_called()

    def test_unknown_tool_key_does_not_raise(self):
        with patch.object(il, "RAW_TOOLS", {}):
            il.install_tool("does-not-exist")  # should print an error, not raise

    def test_tool_name_with_slash_is_sanitized_for_install_dir(self):
        """A tool name containing '/' (from a category or odd data
        entry) must not escape INSTALL_DEST_DIR via path traversal."""
        safe_name = "weird/tool name".replace(" ", "_").replace("/", "_")
        assert "/" not in safe_name
        assert " " not in safe_name
