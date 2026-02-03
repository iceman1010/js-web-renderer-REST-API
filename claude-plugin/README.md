# js-web-renderer Claude Code Plugin

Claude Code plugin providing skills and commands for the js-web-renderer API.

## Prerequisites

The MCP server must be configured in `~/.claude/mcp.json` first. See `../mcp-server/README.md`.

## Installation

Add to your `~/.claude/plugins.json`:

```json
{
  "plugins": [
    "/path/to/js-web-renderer-REST-API/claude-plugin"
  ]
}
```

Or symlink to `~/.claude/plugins/`:

```bash
ln -s /path/to/js-web-renderer-REST-API/claude-plugin ~/.claude/plugins/js-web-renderer
```

## Commands

| Command | Description |
|---------|-------------|
| `/render <url> [profile]` | Render a JS-heavy page and return HTML |
| `/screenshot <url> [width] [height]` | Take a screenshot of a page |
| `/network <url> [click]` | Capture network requests from a page |

## Skill

The `js-render` skill is automatically available and teaches Claude how to use the js-web-renderer tools effectively for:

- Rendering SPAs and React apps
- Interacting with pages (typing, clicking)
- Finding hidden API endpoints and download URLs
- Managing browser profiles for persistent sessions

## Examples

```
/render https://app.put.io/files/123 putio

/screenshot https://example.com 1920 1080

/network https://somesite.com "button.download"
```
