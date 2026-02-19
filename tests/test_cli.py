import subprocess
import tempfile
import os
import pytest


class TestCLI:
    """Test the js-web-renderer CLI tool."""

    def test_basic_render(self):
        """Test basic HTML rendering."""
        result = subprocess.run(
            ["python3", "/opt/js-web-renderer/bin/fetch-rendered.py", "https://example.com", "--wait", "3"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        assert "<html" in result.stdout.lower() or "example" in result.stdout.lower()

    def test_screenshot(self):
        """Test screenshot generation."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            screenshot_path = f.name
        
        try:
            result = subprocess.run(
                ["python3", "/opt/js-web-renderer/bin/fetch-rendered.py", "https://example.com", 
                 "--screenshot", screenshot_path, "--wait", "3"],
                capture_output=True,
                text=True,
                timeout=30
            )
            assert result.returncode == 0
            assert os.path.exists(screenshot_path)
            assert os.path.getsize(screenshot_path) > 0
        finally:
            if os.path.exists(screenshot_path):
                os.unlink(screenshot_path)

    def test_network_capture(self):
        """Test network request capture."""
        result = subprocess.run(
            ["python3", "/opt/js-web-renderer/bin/fetch-rendered.py", "https://example.com", 
             "--only-network", "--wait", "3"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        # Network output should contain URLs
        assert "example.com" in result.stdout

    def test_console_output(self):
        """Test console log capture."""
        result = subprocess.run(
            ["python3", "/opt/js-web-renderer/bin/fetch-rendered.py", "https://example.com", 
             "--console", "--wait", "3"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        # Should complete without errors

    def test_help(self):
        """Test help output."""
        result = subprocess.run(
            ["python3", "/opt/js-web-renderer/bin/fetch-rendered.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0
        assert "--wait" in result.stdout
        assert "--screenshot" in result.stdout
