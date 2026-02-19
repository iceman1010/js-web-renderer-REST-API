from typing import Optional
from pydantic import BaseModel, Field


class TypeAction(BaseModel):
    selector: str = Field(..., description="CSS selector for the input element")
    value: str = Field(..., description="Value to type into the element")


class RenderRequest(BaseModel):
    url: str = Field(..., description="URL to render")
    wait: int = Field(default=5, ge=0, le=60, description="Seconds to wait for page load")
    profile: Optional[str] = Field(default=None, description="Profile name for session persistence")
    type_actions: Optional[list[TypeAction]] = Field(
        default=None, description="List of type actions to perform"
    )
    click_actions: Optional[list[str]] = Field(
        default=None, description="List of CSS selectors to click"
    )
    post_wait: Optional[int] = Field(
        default=None, ge=0, le=120, description="Seconds to wait after actions"
    )
    exec_js: Optional[str] = Field(
        default=None, description="JavaScript to execute before page load"
    )
    post_js: Optional[str] = Field(
        default=None, description="JavaScript to execute after actions"
    )


class RenderResponse(BaseModel):
    success: bool
    html: Optional[str] = None
    current_url: Optional[str] = None
    error: Optional[str] = None


class ScreenshotRequest(BaseModel):
    url: str = Field(..., description="URL to render")
    wait: int = Field(default=5, ge=0, le=60, description="Seconds to wait for page load")
    width: int = Field(default=1280, ge=320, le=3840, description="Viewport width")
    height: int = Field(default=900, ge=240, le=2160, description="Viewport height")
    profile: Optional[str] = Field(default=None, description="Profile name for session persistence")
    type_actions: Optional[list[TypeAction]] = Field(
        default=None, description="List of type actions to perform"
    )
    click_actions: Optional[list[str]] = Field(
        default=None, description="List of CSS selectors to click"
    )
    post_wait: Optional[int] = Field(
        default=None, ge=0, le=120, description="Seconds to wait after actions"
    )
    exec_js: Optional[str] = Field(
        default=None, description="JavaScript to execute before page load"
    )
    post_js: Optional[str] = Field(
        default=None, description="JavaScript to execute after actions"
    )


class NetworkRequest(BaseModel):
    url: str = Field(..., description="URL to render")
    wait: int = Field(default=5, ge=0, le=60, description="Seconds to wait for page load")
    profile: Optional[str] = Field(default=None, description="Profile name for session persistence")
    type_actions: Optional[list[TypeAction]] = Field(
        default=None, description="List of type actions to perform"
    )
    click_actions: Optional[list[str]] = Field(
        default=None, description="List of CSS selectors to click"
    )
    post_wait: Optional[int] = Field(
        default=None, ge=0, le=120, description="Seconds to wait after actions"
    )
    exec_js: Optional[str] = Field(
        default=None, description="JavaScript to execute before page load"
    )
    post_js: Optional[str] = Field(
        default=None, description="JavaScript to execute after actions"
    )


class NetworkResponse(BaseModel):
    success: bool
    requests: Optional[list[dict]] = None
    current_url: Optional[str] = None
    error: Optional[str] = None


class ProfileCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$")


class ProfileInfo(BaseModel):
    name: str
    path: str
    exists: bool
    size_bytes: Optional[int] = None
    last_modified: Optional[str] = None


class ProfileCreateResponse(BaseModel):
    success: bool
    name: str
    path: str


class ProfileListResponse(BaseModel):
    profiles: list[str]


class HealthResponse(BaseModel):
    status: str
    renderer_available: bool
    active_instances: int
    max_instances: int
