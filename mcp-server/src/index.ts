#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";

// Configuration from environment
const API_URL = process.env.JS_RENDER_API_URL || "http://aiworker1.int.opensubtitles.org:9000";
const API_KEY = process.env.JS_RENDER_API_KEY || "";

interface TypeAction {
  selector: string;
  value: string;
}

interface RenderOptions {
  url: string;
  wait?: number;
  profile?: string;
  type_actions?: TypeAction[];
  click_actions?: string[];
  post_wait?: number;
  exec_js?: string;
  post_js?: string;
}

interface ScreenshotOptions extends RenderOptions {
  width?: number;
  height?: number;
}

// API client functions
async function apiRequest(
  method: string,
  endpoint: string,
  data?: unknown,
  auth = true
): Promise<unknown> {
  const url = `${API_URL}${endpoint}`;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (auth && API_KEY) {
    headers["X-API-Key"] = API_KEY;
  }

  const options: RequestInit = {
    method,
    headers,
  };

  if (data && (method === "POST" || method === "PUT")) {
    options.body = JSON.stringify(data);
  }

  const response = await fetch(url, options);

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error((error as { error?: string }).error || `HTTP ${response.status}`);
  }

  // Check if response is binary (screenshot)
  const contentType = response.headers.get("content-type");
  if (contentType?.includes("image/")) {
    const buffer = await response.arrayBuffer();
    return { binary: true, data: Buffer.from(buffer).toString("base64") };
  }

  return response.json();
}

async function renderPage(options: RenderOptions) {
  return apiRequest("POST", "/render", options);
}

async function takeScreenshot(options: ScreenshotOptions) {
  return apiRequest("POST", "/screenshot", options);
}

async function getNetworkRequests(options: RenderOptions) {
  return apiRequest("POST", "/network", options);
}

async function listProfiles() {
  return apiRequest("GET", "/profiles");
}

async function createProfile(name: string) {
  return apiRequest("POST", "/profiles", { name });
}

async function getProfile(name: string) {
  return apiRequest("GET", `/profiles/${encodeURIComponent(name)}`);
}

async function deleteProfile(name: string) {
  return apiRequest("DELETE", `/profiles/${encodeURIComponent(name)}`);
}

async function healthCheck() {
  return apiRequest("GET", "/health", undefined, false);
}

// Tool definitions
const tools: Tool[] = [
  {
    name: "render_page",
    description:
      "Render a JavaScript-heavy web page and return the fully rendered HTML. Useful for SPAs, React apps, and pages that require JS execution to display content.",
    inputSchema: {
      type: "object",
      properties: {
        url: { type: "string", description: "URL to render" },
        wait: {
          type: "number",
          description: "Seconds to wait for page to load (default: 5)",
        },
        profile: {
          type: "string",
          description: "Browser profile name for persistent sessions/cookies",
        },
        type_actions: {
          type: "array",
          items: {
            type: "object",
            properties: {
              selector: { type: "string", description: "CSS selector" },
              value: { type: "string", description: "Text to type" },
            },
            required: ["selector", "value"],
          },
          description: "Text input actions to perform",
        },
        click_actions: {
          type: "array",
          items: { type: "string" },
          description: "CSS selectors of elements to click",
        },
        post_wait: {
          type: "number",
          description: "Seconds to wait after interactions",
        },
        exec_js: {
          type: "string",
          description: "JavaScript to execute before waiting",
        },
        post_js: {
          type: "string",
          description: "JavaScript to execute after waiting",
        },
      },
      required: ["url"],
    },
  },
  {
    name: "screenshot",
    description:
      "Take a screenshot of a web page. Returns base64-encoded PNG image.",
    inputSchema: {
      type: "object",
      properties: {
        url: { type: "string", description: "URL to screenshot" },
        wait: {
          type: "number",
          description: "Seconds to wait for page to load (default: 5)",
        },
        width: {
          type: "number",
          description: "Viewport width in pixels (default: 1280)",
        },
        height: {
          type: "number",
          description: "Viewport height in pixels (default: 900)",
        },
        profile: {
          type: "string",
          description: "Browser profile name for persistent sessions/cookies",
        },
        type_actions: {
          type: "array",
          items: {
            type: "object",
            properties: {
              selector: { type: "string" },
              value: { type: "string" },
            },
            required: ["selector", "value"],
          },
          description: "Text input actions to perform",
        },
        click_actions: {
          type: "array",
          items: { type: "string" },
          description: "CSS selectors of elements to click",
        },
        post_wait: {
          type: "number",
          description: "Seconds to wait after interactions",
        },
        exec_js: { type: "string", description: "JavaScript to execute before waiting" },
        post_js: { type: "string", description: "JavaScript to execute after waiting" },
      },
      required: ["url"],
    },
  },
  {
    name: "network_requests",
    description:
      "Capture all network requests made while loading a page. Useful for finding API endpoints, download URLs, etc.",
    inputSchema: {
      type: "object",
      properties: {
        url: { type: "string", description: "URL to analyze" },
        wait: {
          type: "number",
          description: "Seconds to wait for page to load (default: 5)",
        },
        profile: {
          type: "string",
          description: "Browser profile name for persistent sessions/cookies",
        },
        type_actions: {
          type: "array",
          items: {
            type: "object",
            properties: {
              selector: { type: "string" },
              value: { type: "string" },
            },
            required: ["selector", "value"],
          },
          description: "Text input actions to perform",
        },
        click_actions: {
          type: "array",
          items: { type: "string" },
          description: "CSS selectors of elements to click",
        },
        post_wait: {
          type: "number",
          description: "Seconds to wait after interactions",
        },
        exec_js: { type: "string", description: "JavaScript to execute before waiting" },
        post_js: { type: "string", description: "JavaScript to execute after waiting" },
      },
      required: ["url"],
    },
  },
  {
    name: "list_profiles",
    description: "List all available browser profiles",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
  {
    name: "create_profile",
    description:
      "Create a new browser profile for persistent sessions and cookies",
    inputSchema: {
      type: "object",
      properties: {
        name: { type: "string", description: "Profile name" },
      },
      required: ["name"],
    },
  },
  {
    name: "get_profile",
    description: "Get information about a specific browser profile",
    inputSchema: {
      type: "object",
      properties: {
        name: { type: "string", description: "Profile name" },
      },
      required: ["name"],
    },
  },
  {
    name: "delete_profile",
    description: "Delete a browser profile",
    inputSchema: {
      type: "object",
      properties: {
        name: { type: "string", description: "Profile name" },
      },
      required: ["name"],
    },
  },
  {
    name: "health",
    description: "Check if the js-web-renderer API is healthy",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
];

// Create server
const server = new Server(
  {
    name: "js-web-renderer",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Handle tool listing
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools,
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let result: unknown;

    switch (name) {
      case "render_page":
        result = await renderPage(args as unknown as RenderOptions);
        break;
      case "screenshot":
        result = await takeScreenshot(args as unknown as ScreenshotOptions);
        break;
      case "network_requests":
        result = await getNetworkRequests(args as unknown as RenderOptions);
        break;
      case "list_profiles":
        result = await listProfiles();
        break;
      case "create_profile":
        result = await createProfile((args as { name: string }).name);
        break;
      case "get_profile":
        result = await getProfile((args as { name: string }).name);
        break;
      case "delete_profile":
        result = await deleteProfile((args as { name: string }).name);
        break;
      case "health":
        result = await healthCheck();
        break;
      default:
        throw new Error(`Unknown tool: ${name}`);
    }

    // Handle screenshot binary response
    const binaryResult = result as { binary?: boolean; data?: string } | null;
    if (binaryResult?.binary && binaryResult.data) {
      return {
        content: [
          {
            type: "image",
            data: binaryResult.data,
            mimeType: "image/png",
          },
        ],
      };
    }

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error instanceof Error ? error.message : String(error)}`,
        },
      ],
      isError: true,
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("js-web-renderer MCP server running on stdio");
}

main().catch(console.error);
