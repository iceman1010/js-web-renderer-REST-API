# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI REST API server that wraps the `js-web-renderer` CLI tool, exposing its JavaScript-heavy web page rendering capabilities through HTTP endpoints with API key authentication.

## Production Server

Deployed on **aiworker1.int.opensubtitles.org** (port 9000). See server documentation: `/home/iceman/Documents/projects/Claude/ai.opensubtitles.com/docs/whisper1.md`

## Development Commands

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run development server
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 9000

# Run with auto-reload during development
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload

# Production deployment (systemd)
./install.sh                              # Full install to /opt/js-web-renderer-api
systemctl start js-web-renderer-api
systemctl status js-web-renderer-api
journalctl -u js-web-renderer-api -f      # View logs
```

## Architecture

### Request Flow
```
HTTP Request → FastAPI Router → Auth Middleware → Pydantic Validation → renderer.run_renderer() → subprocess(js-web-renderer CLI) → Parse Output → JSON Response
```

### Key Components

- **app/main.py**: FastAPI app with 8 endpoints (render, screenshot, network, profiles CRUD, health, docs)
- **app/renderer.py**: Async wrapper that builds CLI args and executes `js-web-renderer` subprocess
- **app/models.py**: Pydantic v2 request/response models with validation
- **app/auth.py**: API key header authentication (`X-API-Key`)
- **app/config.py**: Settings from `.env` file (API_KEY, PROFILES_DIR, JS_WEB_RENDERER_PATH, HOST, PORT)

### External Dependency

The API requires `js-web-renderer` CLI installed at the path specified in `JS_WEB_RENDERER_PATH` (default: `/opt/js-web-renderer/bin/fetch-rendered.py`). The renderer handles headless browser operations.

### CLI Argument Building

`renderer.py` translates API request fields to CLI flags:
- `--wait`, `--post-wait` for timing
- `--profile <path>` for session persistence
- `--type <selector>::<value>` for text input (note double colon separator)
- `--click <selector>` for clicking elements
- `--exec-js`, `--post-js` for JavaScript execution
- `--screenshot <path>`, `--width`, `--height` for screenshots
- `--only-network` for network request capture

### Profile System

Browser profiles are stored in `PROFILES_DIR` (default: `/opt/js-web-renderer/profiles`). Profiles persist cookies/session state across multiple API requests.

## API Testing

```bash
# Health check (no auth)
curl http://localhost:9000/health

# Render page
curl -X POST http://localhost:9000/render \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "wait": 5}'

# Screenshot
curl -X POST http://localhost:9000/screenshot \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "width": 1280, "height": 900}' \
  --output screenshot.png
```
