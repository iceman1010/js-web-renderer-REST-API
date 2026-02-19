import asyncio
import json
import shlex
import tempfile
from pathlib import Path
from typing import Optional

from .config import settings
from .models import TypeAction


class RendererError(Exception):
    pass


class ConcurrencyLimitError(RendererError):
    pass


_active_instances = 0


async def run_renderer(
    url: str,
    wait: int = 5,
    profile: Optional[str] = None,
    type_actions: Optional[list[TypeAction]] = None,
    click_actions: Optional[list[str]] = None,
    post_wait: Optional[int] = None,
    exec_js: Optional[str] = None,
    post_js: Optional[str] = None,
    screenshot: bool = False,
    width: int = 1280,
    height: int = 900,
    network: bool = False,
) -> dict:
    """Run js-web-renderer and return results."""
    
    global _active_instances
    if _active_instances >= settings.MAX_INSTANCES:
        raise ConcurrencyLimitError(f"Too many concurrent render requests. Limit is {settings.MAX_INSTANCES}.")
        
    _active_instances += 1
    
    try:
        cmd = [
        str(settings.JS_WEB_RENDERER_PATH),
        url,
        "--wait", str(wait),
        ]

        if profile:
            profile_path = settings.PROFILES_DIR / profile
            cmd.extend(["--profile", str(profile_path)])

        if type_actions:
            for action in type_actions:
                cmd.extend(["--type", f"{action.selector}::{action.value}"])

        if click_actions:
            for selector in click_actions:
                cmd.extend(["--click", selector])

        if post_wait is not None:
            cmd.extend(["--post-wait", str(post_wait)])

        if exec_js:
            cmd.extend(["--exec-js", exec_js])

        if post_js:
            cmd.extend(["--post-js", post_js])

        screenshot_file = None

        if screenshot:
            screenshot_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            screenshot_file.close()
            cmd.extend([
                "--screenshot", screenshot_file.name,
                "--width", str(width),
                "--height", str(height),
                ])

        if network:
            cmd.append("--only-network")

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=max(wait + (post_wait or 0) + 60, 120)
                )
            except (asyncio.TimeoutError, asyncio.CancelledError):
                if process.returncode is None:
                    try:
                        process.kill()
                    except ProcessLookupError:
                        pass
                raise

            if process.returncode != 0:
                error_msg = stderr.decode().strip() or f"Renderer exited with code {process.returncode}"
                raise RendererError(error_msg)

            output = stdout.decode()

            result = {
                "success": True,
                "html": None,
                "current_url": None,
            }

            # Handle network output (--only-network returns network requests as text)
            if network:
                # Parse network log output - each line is a request URL
                requests = []
                for line in output.strip().split("\n"):
                    line = line.strip()
                    if line:
                        requests.append({"url": line})
                result["network_data"] = requests
            elif screenshot:
                # Screenshot mode - no HTML output
                pass
            else:
                # Normal HTML output
                if output.startswith("CURRENT_URL:"):
                    lines = output.split("\n", 1)
                    result["current_url"] = lines[0].replace("CURRENT_URL:", "").strip()
                    result["html"] = lines[1] if len(lines) > 1 else ""
                else:
                    result["html"] = output

            if screenshot and screenshot_file:
                screenshot_path = Path(screenshot_file.name)
                if screenshot_path.exists():
                    result["screenshot_data"] = screenshot_path.read_bytes()
                    screenshot_path.unlink()
                else:
                    raise RendererError("Screenshot file was not created")

            return result

        except asyncio.TimeoutError:
            raise RendererError("Renderer timed out")
        except Exception as e:
            if isinstance(e, RendererError):
                raise
            raise RendererError(str(e))
        finally:
            # Clean up temp files on error
            if screenshot_file:
                try:
                    Path(screenshot_file.name).unlink(missing_ok=True)
                except:
                    pass
    finally:
        _active_instances -= 1


def is_renderer_available() -> bool:
    """Check if the renderer script exists and is executable."""
    path = settings.JS_WEB_RENDERER_PATH
    return path.exists() and path.is_file()


def get_active_instances() -> int:
    """Get the current number of active browser instances."""
    return _active_instances
