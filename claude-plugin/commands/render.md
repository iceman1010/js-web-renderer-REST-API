---
description: Render a JavaScript-heavy web page and return the HTML
arguments:
  - name: url
    description: URL to render
    required: true
  - name: profile
    description: Browser profile name (optional)
    required: false
---

Render the web page at `$ARGUMENTS.url` using the js-web-renderer MCP tools.

{{#if $ARGUMENTS.profile}}
Use the browser profile: `$ARGUMENTS.profile`
{{/if}}

Steps:
1. Call `mcp__js-web-renderer__render_page` with:
   - url: $ARGUMENTS.url
   - wait: 5 (adjust if page is slow)
   {{#if $ARGUMENTS.profile}}- profile: $ARGUMENTS.profile{{/if}}

2. If successful, summarize what was rendered:
   - Page title
   - Key content found
   - Any relevant data extracted

3. If the user needs specific data, help extract it from the HTML response.
