---
name: js-render
description: Render JavaScript-heavy web pages using the js-web-renderer MCP tools. Use when the user needs to fetch content from SPAs, React apps, or pages requiring JS execution.
---

# JS Web Renderer Skill

You have access to MCP tools for rendering JavaScript-heavy web pages via a headless browser.

## Available Tools

Use these MCP tools (prefixed with `mcp__js-web-renderer__`):

| Tool | Purpose |
|------|---------|
| `render_page` | Get fully rendered HTML from a JS-heavy page |
| `screenshot` | Capture a PNG screenshot of a page |
| `network_requests` | Capture all network requests (useful for finding APIs/download URLs) |
| `list_profiles` | List browser profiles |
| `create_profile` | Create a profile for persistent sessions |
| `delete_profile` | Remove a profile |

## Common Workflows

### 1. Render a Page and Extract Data

```
1. Use render_page with the URL
2. Parse the returned HTML to extract the data you need
3. Use regex or string matching to find specific content
```

### 2. Interact with a Page (Login, Click Buttons)

```
1. Create a profile if you need persistent sessions: create_profile
2. Use render_page with:
   - type_actions: [{ selector: "input#email", value: "user@example.com" }]
   - click_actions: ["button.submit"]
   - post_wait: 3 (wait for action to complete)
3. The profile preserves cookies for subsequent requests
```

### 3. Find Hidden API Endpoints or Download URLs

```
1. Use network_requests with the URL
2. Optionally add click_actions to trigger the download/API call
3. Search the network requests for the URL pattern you need
```

### 4. Screenshot for Debugging

```
1. Use screenshot with width/height for viewport size
2. The tool returns a base64 PNG image
```

## Tips

- **Profiles**: Use profiles when you need to maintain login state across multiple requests
- **Wait times**: Increase `wait` for slow-loading pages, use `post_wait` after interactions
- **Selectors**: Use CSS selectors for type_actions and click_actions
- **JavaScript**: Use `exec_js` to run code before waiting, `post_js` after waiting
