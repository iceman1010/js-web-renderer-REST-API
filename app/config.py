import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:
    API_KEY: str = os.getenv("API_KEY", "")
    PROFILES_DIR: Path = Path(os.getenv("PROFILES_DIR", "/opt/js-web-renderer/profiles"))
    JS_WEB_RENDERER_PATH: Path = Path(
        os.getenv("JS_WEB_RENDERER_PATH", "/opt/js-web-renderer/bin/fetch-rendered.py")
    )
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "9000"))
    MAX_INSTANCES: int = int(os.getenv("MAX_INSTANCES", "4"))


settings = Settings()
