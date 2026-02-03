---
description: Capture network requests from loading a page (find APIs, download URLs)
arguments:
  - name: url
    description: URL to analyze
    required: true
  - name: click
    description: CSS selector to click (optional, to trigger additional requests)
    required: false
---

Capture network requests from `$ARGUMENTS.url` using the js-web-renderer MCP tools.

Call `mcp__js-web-renderer__network_requests` with:
- url: $ARGUMENTS.url
- wait: 5
{{#if $ARGUMENTS.click}}
- click_actions: ["$ARGUMENTS.click"]
- post_wait: 3
{{/if}}

After getting results:
1. List the most interesting requests (APIs, downloads, data endpoints)
2. Filter out static assets (images, CSS, fonts) unless specifically asked
3. Highlight any authentication tokens or interesting parameters in URLs
