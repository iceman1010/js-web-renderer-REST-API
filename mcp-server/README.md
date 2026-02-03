# js-web-renderer MCP Server

MCP (Model Context Protocol) server that exposes the js-web-renderer REST API as tools for Claude.

## Tools

| Tool | Description |
|------|-------------|
| `render_page` | Render a JavaScript-heavy web page and return fully rendered HTML |
| `screenshot` | Take a screenshot of a web page (returns base64 PNG) |
| `network_requests` | Capture all network requests made while loading a page |
| `list_profiles` | List available browser profiles |
| `create_profile` | Create a new browser profile for persistent sessions |
| `get_profile` | Get information about a specific profile |
| `delete_profile` | Delete a browser profile |
| `health` | Check API health status |

## Installation

```bash
cd mcp-server
npm install
npm run build
```

## Configuration

Set environment variables:

```bash
export JS_RENDER_API_URL="http://aiworker1.int.opensubtitles.org:9000"
export JS_RENDER_API_KEY="your-api-key"
```

## Usage with Claude Code

Add to your `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "js-web-renderer": {
      "command": "node",
      "args": ["/path/to/js-web-renderer-REST-API/mcp-server/dist/index.js"],
      "env": {
        "JS_RENDER_API_URL": "http://aiworker1.int.opensubtitles.org:9000",
        "JS_RENDER_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Example Usage

Once configured, Claude can use these tools:

```
"Render https://app.put.io/files/123 using the 'putio' profile and click the download button"

"Take a screenshot of https://example.com with viewport 1920x1080"

"Capture network requests from https://somesite.com to find the API endpoints"
```
