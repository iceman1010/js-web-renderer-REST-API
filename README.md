# js-web-renderer REST API

REST API for rendering JavaScript-heavy web pages using js-web-renderer.

## Features

- Render pages and return HTML content
- Take screenshots
- Capture network requests
- Session persistence with browser profiles
- API key authentication

## Installation

### Quick Install (on target server)

```bash
git clone https://github.com/yourusername/js-web-renderer-REST-API.git
cd js-web-renderer-REST-API
chmod +x install.sh
./install.sh
```

### Manual Install

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Create `.env` from example:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Run the server:
```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 9000
```

## Configuration

Edit `.env`:

```
API_KEY=your-secret-api-key
PROFILES_DIR=/opt/js-web-renderer/profiles
JS_WEB_RENDERER_PATH=/opt/js-web-renderer/bin/fetch-rendered.py
HOST=0.0.0.0
PORT=9000
```

## API Endpoints

### Rendering

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/render` | Render page, return HTML + current URL |
| `POST` | `/screenshot` | Render page, return PNG image |
| `POST` | `/network` | Render page, return network requests |

### Profiles

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/profiles` | List all saved profiles |
| `POST` | `/profiles` | Create a new empty profile |
| `GET` | `/profiles/{name}` | Get profile info |
| `DELETE` | `/profiles/{name}` | Delete a profile |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check (no auth required) |
| `GET` | `/docs` | OpenAPI documentation |

## Authentication

All endpoints except `/health` require an API key in the `X-API-Key` header.

## Usage Examples

### Render a page

```bash
curl -X POST http://localhost:9000/render \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "wait": 5}'
```

### Take a screenshot

```bash
curl -X POST http://localhost:9000/screenshot \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "wait": 5, "width": 1280, "height": 900}' \
  --output screenshot.png
```

### Login and save session

```bash
# Create profile
curl -X POST http://localhost:9000/profiles \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-session"}'

# Login with profile
curl -X POST http://localhost:9000/render \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/login",
    "wait": 5,
    "profile": "my-session",
    "type_actions": [
      {"selector": "input[name=username]", "value": "myuser"},
      {"selector": "input[name=password]", "value": "mypass"}
    ],
    "click_actions": ["button[type=submit]"],
    "post_wait": 10
  }'

# Use saved session
curl -X POST http://localhost:9000/render \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/dashboard", "wait": 5, "profile": "my-session"}'
```

### Capture network requests

```bash
curl -X POST http://localhost:9000/network \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "wait": 5}'
```

## Request Parameters

### Common Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | required | URL to render |
| `wait` | int | 5 | Seconds to wait for page load (0-60) |
| `profile` | string | null | Profile name for session persistence |
| `type_actions` | array | null | List of `{selector, value}` to type |
| `click_actions` | array | null | List of CSS selectors to click |
| `post_wait` | int | null | Seconds to wait after actions (0-120) |
| `exec_js` | string | null | JavaScript to execute before load |
| `post_js` | string | null | JavaScript to execute after actions |

### Screenshot Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `width` | int | 1280 | Viewport width (320-3840) |
| `height` | int | 900 | Viewport height (240-2160) |

## License

MIT
