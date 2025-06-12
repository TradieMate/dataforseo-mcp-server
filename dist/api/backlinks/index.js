"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.registerBacklinksTools = registerBacklinksTools;
const zod_1 = require("zod");
const tools_js_1 = require("../tools.js");
// Backlinks API schemas
const targetSchema = {
    target: zod_1.z.string().describe("Target domain, subdomain or URL to analyze"),
    limit: zod_1.z.number().optional().describe("Maximum number of results to return"),
    offset: zod_1.z.number().optional().describe("Offset for pagination"),
    filters: zod_1.z.array(zod_1.z.any()).optional().describe("Array of filter objects")
};
function registerBacklinksTools(server, apiClient) {
    // Backlinks Summary
    (0, tools_js_1.registerTool)(server, "backlinks_summary", targetSchema, async (params, apiClient) => {
        const response = await apiClient.post("/backlinks/summary/live", [params]);
        return response;
    }, apiClient);
    // Backlinks List
    (0, tools_js_1.registerTool)(server, "backlinks_backlinks", { ...targetSchema,
        mode: zod_1.z.enum(["as_is", "as_csv"]).optional().describe("Data presentation mode"),
    }, async (params, client) => {
        const response = await apiClient.post("/backlinks/backlinks/live", [params]);
        return response;
    }, apiClient);
    // Anchors
    (0, tools_js_1.registerTool)(server, "backlinks_anchors", targetSchema, async (params, apiClient) => {
        const response = await apiClient.post("/backlinks/anchors/live", [params]);
        return response;
    }, apiClient);
    // Backlinks Domain Pages
    (0, tools_js_1.registerTool)(server, "backlinks_domain_pages", targetSchema, async (params, apiClient) => {
        const response = await apiClient.post("/backlinks/domain_pages/live", [params]);
        return response;
    }, apiClient);
    // Domain Pages Summary
    (0, tools_js_1.registerTool)(server, "backlinks_domain_pages_summary", targetSchema, async (params, apiClient) => {
        const response = await apiClient.post("/backlinks/domain_pages_summary/live", [params]);
        return response;
    }, apiClient);
    // Referring Domains
    (0, tools_js_1.registerTool)(server, "backlinks_referring_domains", targetSchema, async (params, apiClient) => {
        const response = await apiClient.post("/backlinks/referring_domains/live", [params]);
        return response;
    }, apiClient);
    // Referring Networks
    (0, tools_js_1.registerTool)(server, "backlinks_referring_networks", targetSchema, async (params, apiClient) => {
        const response = await apiClient.post("/backlinks/referring_networks/live", [params]);
        return response;
    }, apiClient);
    // Bulk Backlinks
    (0, tools_js_1.registerTool)(server, "backlinks_bulk_backlinks", {
        targets: zod_1.z.array(zod_1.z.string()).describe("List of targets to analyze (domains, subdomains, URLs)"),
        limit: zod_1.z.number().optional().describe("Maximum number of results to return per target"),
        offset: zod_1.z.number().optional().describe("Offset for pagination"),
        internal_list_limit: zod_1.z.number().optional().describe("Maximum number of items in internal lists per target")
    }, async (params, client) => {
        const response = await apiClient.post("/backlinks/bulk_backlinks/live", [params]);
        return response;
    }, apiClient);
    // Bulk Referring Domains
    (0, tools_js_1.registerTool)(server, "backlinks_bulk_referring_domains", {
        targets: zod_1.z.array(zod_1.z.string()).describe("List of targets to analyze (domains, subdomains, URLs)"),
        limit: zod_1.z.number().optional().describe("Maximum number of results to return per target"),
        offset: zod_1.z.number().optional().describe("Offset for pagination"),
        internal_list_limit: zod_1.z.number().optional().describe("Maximum number of items in internal lists per target")
    }, async (params, client) => {
        const response = await apiClient.post("/backlinks/bulk_referring_domains/live", [params]);
        return response;
    }, apiClient);
    // Bulk Spam Score
    (0, tools_js_1.registerTool)(server, "backlinks_bulk_spam_score", {
        targets: zod_1.z.array(zod_1.z.string()).describe("List of targets to analyze (domains, subdomains, URLs)")
    }, async (params, client) => {
        const response = await apiClient.post("/backlinks/bulk_spam_score/live", [params]);
        return response;
    }, apiClient);
    // Bulk Rank Overview
    (0, tools_js_1.registerTool)(server, "backlinks_bulk_ranks", {
        targets: zod_1.z.array(zod_1.z.string()).describe("List of targets to analyze (domains, subdomains, URLs)")
    }, async (params, client) => {
        const response = await apiClient.post("/backlinks/bulk_ranks/live", [params]);
        return response;
    }, apiClient);
    // Domain Competitors
    (0, tools_js_1.registerTool)(server, "backlinks_competitors", targetSchema, async (params, apiClient) => {
        const response = await apiClient.post("/backlinks/competitors/live", [params]);
        return response;
    }, apiClient);
    // Domain Intersection
    (0, tools_js_1.registerTool)(server, "backlinks_domain_intersection", {
        targets: zod_1.z.array(zod_1.z.string()).min(2).max(20).describe("List of domains to compare"),
        limit: zod_1.z.number().optional().describe("Maximum number of results to return"),
        offset: zod_1.z.number().optional().describe("Offset for pagination"),
        exclude_targets: zod_1.z.boolean().optional().describe("Whether to exclude the target domains from the results")
    }, async (params, client) => {
        const response = await apiClient.post("/backlinks/domain_intersection/live", [params]);
        return response;
    }, apiClient);
    // Page Intersection
    (0, tools_js_1.registerTool)(server, "backlinks_page_intersection", {
        targets: zod_1.z.array(zod_1.z.string()).min(2).max(20).describe("List of URLs to compare"),
        limit: zod_1.z.number().optional().describe("Maximum number of results to return"),
        offset: zod_1.z.number().optional().describe("Offset for pagination"),
        exclude_targets: zod_1.z.boolean().optional().describe("Whether to exclude the target URLs from the results")
    }, async (params, client) => {
        const response = await apiClient.post("/backlinks/page_intersection/live", [params]);
        return response;
    }, apiClient);
    // Timeseries New Lost Summary
    (0, tools_js_1.registerTool)(server, "backlinks_timeseries_new_lost_summary", { ...targetSchema,
        date_from: zod_1.z.string().describe("Start date in YYYY-MM-DD format"),
        date_to: zod_1.z.string().describe("End date in YYYY-MM-DD format")
    }, async (params, client) => {
        const response = await apiClient.post("/backlinks/timeseries_new_lost_summary/live", [params]);
        return response;
    }, apiClient);
    // Backlinks Index
    (0, tools_js_1.registerTool)(server, "backlinks_index", {}, async (_params, client) => {
        const response = await apiClient.get("/backlinks/index");
        return response;
    }, apiClient);
    // Backlinks Status
    (0, tools_js_1.registerTool)(server, "backlinks_errors", {}, async (_params, client) => {
        const response = await apiClient.get("/backlinks/errors");
        return response;
    }, apiClient);
}
//# sourceMappingURL=index.js.map