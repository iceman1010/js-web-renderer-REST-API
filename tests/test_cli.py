import subprocess
import tempfile
import os
import pytest


# Test CLI on remote server via SSH
CLI_PATH = "/opt/js-web-renderer/bin/fetch-rendered.py"
REMOTE_HOST = "whisper1"


def run_remote_command(cmd):
    """Run a command on the remote server via SSH."""
    result = subprocess.run(
        ["ssh", REMOTE_HOST, cmd],
        capture_output=True,
        text=True,
        timeout=60
    )
    return result


class TestCLI:
    """Test the js-web-renderer CLI tool on the server."""

    def test_basic_render(self):
        """Test basic HTML rendering."""
        result = run_remote_command(f"python3 {CLI_PATH} https://example.com --wait 3")
        assert result.returncode == 0
        assert "<html" in result.stdout.lower() or "example" in result.stdout.lower()

    def test_screenshot(self):
        """Test screenshot generation."""
        screenshot_path = f"/tmp/test_screenshot_{os.urandom(4).hex()}.png"
        
        result = run_remote_command(f"python3 {CLI_PATH} https://example.com --screenshot {screenshot_path} --wait 3")
        
        # Check if screenshot was created
        check = run_remote_command(f"ls -la {screenshot_path}")
        assert check.returncode == 0
        assert "example.com" not in check.stdout or "No such file" not in check.stdout
        
        # Cleanup
        run_remote_command(f"rm -f {screenshot_path}")

    def test_network_capture(self):
        """Test network request capture."""
        result = run_remote_command(f"python3 {CLI_PATH} https://example.com --only-network --wait 3")
        assert result.returncode == 0
        # Network output should contain URLs
        assert "example.com" in result.stdout

    def test_console_output(self):
        """Test console log capture."""
        result = run_remote_command(f"python3 {CLI_PATH} https://example.com --console --wait 3")
        assert result.returncode == 0
        # Should complete without errors

    def test_help(self):
        """Test help output."""
        result = run_remote_command(f"python3 {CLI_PATH} --help")
        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert "--wait" in output
        assert "--screenshot" in output
