import os
import shutil
from datetime import datetime
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import Response

from .auth import verify_api_key
from .config import settings
from .models import (
    HealthResponse,
    NetworkRequest,
    NetworkResponse,
    ProfileCreateRequest,
    ProfileCreateResponse,
    ProfileInfo,
    ProfileListResponse,
    RenderRequest,
    RenderResponse,
    ScreenshotRequest,
)
from .renderer import RendererError, is_renderer_available, run_renderer

app = FastAPI(
    title="js-web-renderer REST API",
    description="REST API for rendering JavaScript-heavy web pages",
    version="1.0.0",
)


# Health check (no auth required)
@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        renderer_available=is_renderer_available(),
    )


# Rendering endpoints
@app.post("/render", response_model=RenderResponse, tags=["Rendering"])
async def render_page(
    request: RenderRequest,
    _: str = Depends(verify_api_key),
):
    """Render a page and return HTML content."""
    try:
        result = await run_renderer(
            url=request.url,
            wait=request.wait,
            profile=request.profile,
            type_actions=request.type_actions,
            click_actions=request.click_actions,
            post_wait=request.post_wait,
            exec_js=request.exec_js,
            post_js=request.post_js,
        )
        return RenderResponse(
            success=True,
            html=result.get("html"),
            current_url=result.get("current_url"),
        )
    except RendererError as e:
        return RenderResponse(success=False, error=str(e))


@app.post("/screenshot", tags=["Rendering"])
async def take_screenshot(
    request: ScreenshotRequest,
    _: str = Depends(verify_api_key),
):
    """Render a page and return a PNG screenshot."""
    try:
        result = await run_renderer(
            url=request.url,
            wait=request.wait,
            profile=request.profile,
            type_actions=request.type_actions,
            click_actions=request.click_actions,
            post_wait=request.post_wait,
            exec_js=request.exec_js,
            post_js=request.post_js,
            screenshot=True,
            width=request.width,
            height=request.height,
        )
        return Response(
            content=result["screenshot_data"],
            media_type="image/png",
        )
    except RendererError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.post("/network", response_model=NetworkResponse, tags=["Rendering"])
async def capture_network(
    request: NetworkRequest,
    _: str = Depends(verify_api_key),
):
    """Render a page and return network requests."""
    try:
        result = await run_renderer(
            url=request.url,
            wait=request.wait,
            profile=request.profile,
            type_actions=request.type_actions,
            click_actions=request.click_actions,
            post_wait=request.post_wait,
            exec_js=request.exec_js,
            post_js=request.post_js,
            network=True,
        )
        return NetworkResponse(
            success=True,
            requests=result.get("network_data"),
            current_url=result.get("current_url"),
        )
    except RendererError as e:
        return NetworkResponse(success=False, error=str(e))


# Profile endpoints
@app.get("/profiles", response_model=ProfileListResponse, tags=["Profiles"])
async def list_profiles(_: str = Depends(verify_api_key)):
    """List all saved profiles."""
    profiles = []
    if settings.PROFILES_DIR.exists():
        for item in settings.PROFILES_DIR.iterdir():
            if item.is_dir():
                profiles.append(item.name)
    return ProfileListResponse(profiles=sorted(profiles))


@app.post("/profiles", response_model=ProfileCreateResponse, tags=["Profiles"])
async def create_profile(
    request: ProfileCreateRequest,
    _: str = Depends(verify_api_key),
):
    """Create a new empty profile."""
    profile_path = settings.PROFILES_DIR / request.name

    if profile_path.exists():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Profile '{request.name}' already exists",
        )

    try:
        settings.PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        profile_path.mkdir()
        return ProfileCreateResponse(
            success=True,
            name=request.name,
            path=str(profile_path),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create profile: {e}",
        )


@app.get("/profiles/{name}", response_model=ProfileInfo, tags=["Profiles"])
async def get_profile(name: str, _: str = Depends(verify_api_key)):
    """Get profile information."""
    profile_path = settings.PROFILES_DIR / name

    if not profile_path.exists():
        return ProfileInfo(
            name=name,
            path=str(profile_path),
            exists=False,
        )

    # Calculate total size
    total_size = 0
    for item in profile_path.rglob("*"):
        if item.is_file():
            total_size += item.stat().st_size

    # Get last modified time
    last_modified = None
    try:
        stat = profile_path.stat()
        last_modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
    except:
        pass

    return ProfileInfo(
        name=name,
        path=str(profile_path),
        exists=True,
        size_bytes=total_size,
        last_modified=last_modified,
    )


@app.delete("/profiles/{name}", tags=["Profiles"])
async def delete_profile(name: str, _: str = Depends(verify_api_key)):
    """Delete a profile."""
    profile_path = settings.PROFILES_DIR / name

    if not profile_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile '{name}' not found",
        )

    try:
        shutil.rmtree(profile_path)
        return {"success": True, "message": f"Profile '{name}' deleted"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete profile: {e}",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )
