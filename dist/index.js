"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const mcp_js_1 = require("@modelcontextprotocol/sdk/server/mcp.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
const client_js_1 = require("./api/client.js");
const index_js_1 = require("./api/serp/index.js");
const index_js_2 = require("./api/keywords/index.js");
const index_js_3 = require("./api/labs/index.js");
const index_js_4 = require("./api/backlinks/index.js");
const index_js_5 = require("./api/onpage/index.js");
const index_js_6 = require("./api/domain-analytics/index.js");
const index_js_7 = require("./api/content-analysis/index.js");
const index_js_8 = require("./api/content-generation/index.js");
const index_js_9 = require("./api/merchant/index.js");
const index_js_10 = require("./api/app-data/index.js");
const index_js_11 = require("./api/business-data/index.js");
async function main() {
    // Get authentication credentials from environment variables
    const dataForSeoLogin = process.env.DATAFORSEO_LOGIN;
    const dataForSeoPassword = process.env.DATAFORSEO_PASSWORD;
    if (!dataForSeoLogin || !dataForSeoPassword) {
        console.error("Error: DataForSEO API credentials not provided");
        console.error("Please set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD environment variables");
        process.exit(1);
    }
    // Setup API client
    const apiClient = (0, client_js_1.setupApiClient)(dataForSeoLogin, dataForSeoPassword);
    // Create an MCP server
    const server = new mcp_js_1.McpServer({
        name: "SEO Tools MCP Server",
        version: "1.0.0",
    });
    // Register tools for each DataForSEO API category
    (0, index_js_1.registerSerpTools)(server, apiClient);
    (0, index_js_2.registerKeywordsTools)(server, apiClient);
    (0, index_js_3.registerLabsTools)(server, apiClient);
    (0, index_js_4.registerBacklinksTools)(server, apiClient);
    (0, index_js_5.registerOnPageTools)(server, apiClient);
    (0, index_js_6.registerDomainAnalyticsTools)(server, apiClient);
    (0, index_js_7.registerContentAnalysisTools)(server, apiClient);
    (0, index_js_8.registerContentGenerationTools)(server, apiClient);
    (0, index_js_9.registerMerchantTools)(server, apiClient);
    (0, index_js_10.registerAppDataTools)(server, apiClient);
    (0, index_js_11.registerBusinessDataTools)(server, apiClient);
    // Register third-party API tools
    // Add more third-party API integrations here as needed
    // Start receiving messages on stdin and sending messages on stdout
    const transport = new stdio_js_1.StdioServerTransport();
    console.error("SEO Tools MCP Server starting...");
    await server.connect(transport);
    console.error("SEO Tools MCP Server connected");
}
main().catch((error) => {
    console.error("Error in SEO Tools MCP Server:", error);
    process.exit(1);
});
//# sourceMappingURL=index.js.map