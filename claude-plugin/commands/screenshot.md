---
description: Take a screenshot of a web page
arguments:
  - name: url
    description: URL to screenshot
    required: true
  - name: width
    description: Viewport width (default 1280)
    required: false
  - name: height
    description: Viewport height (default 900)
    required: false
---

Take a screenshot of `$ARGUMENTS.url` using the js-web-renderer MCP tools.

Call `mcp__js-web-renderer__screenshot` with:
- url: $ARGUMENTS.url
- width: $ARGUMENTS.width or 1280
- height: $ARGUMENTS.height or 900
- wait: 5

The tool will return a base64-encoded PNG image. Display it to the user.
