"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.registerKeywordsTools = registerKeywordsTools;
const zod_1 = require("zod");
const tools_js_1 = require("../tools.js");
function registerKeywordsTools(server, apiClient) {
    // Google Ads Keywords Data
    (0, tools_js_1.registerTool)(server, "keywords_google_ads_keywords_for_keyword", {
        keyword: zod_1.z.string().describe("Keyword to get data for"),
        location_code: zod_1.z.number().optional().describe("The location code for the search"),
        language_code: zod_1.z.string().optional().describe("The language code for the search"),
    }, async (params, client) => {
        const response = await apiClient.post("/keywords_data/google_ads/keywords_for_keywords/live", [params]);
        return response;
    }, apiClient);
    // Google Ads Keywords Suggestions
    (0, tools_js_1.registerTool)(server, "keywords_google_ads_keywords_for_site", {
        target: zod_1.z.string().describe("Target domain, subdomain or URL to analyze"),
        location_code: zod_1.z.number().optional().describe("The location code for the search"),
        language_code: zod_1.z.string().optional().describe("The language code for the search"),
    }, async (params, client) => {
        const response = await apiClient.post("/keywords_data/google_ads/keywords_for_site/live", [params]);
        return response;
    }, apiClient);
    // Google Ads Search Volume
    (0, tools_js_1.registerTool)(server, "keywords_google_ads_search_volume", {
        keywords: zod_1.z.array(zod_1.z.string()).describe("Keywords to get search volume for"),
        location_code: zod_1.z.number().optional().describe("The location code for the search"),
        language_code: zod_1.z.string().optional().describe("The language code for the search"),
    }, async (params, client) => {
        const response = await apiClient.post("/keywords_data/google_ads/search_volume/live", [params]);
        return response;
    }, apiClient);
    // Google Ads Keywords Locations
    (0, tools_js_1.registerTool)(server, "keywords_google_ads_locations", {
        country: zod_1.z.string().optional().describe("Filter locations by country name")
    }, async (params) => {
        const url = params.country
            ? `/keywords_data/google_ads/locations?country=${encodeURIComponent(params.country)}`
            : "/keywords_data/google_ads/locations";
        const response = await apiClient.get(url);
        return response;
    }, apiClient);
    // Google Ads Keywords Languages
    (0, tools_js_1.registerTool)(server, "keywords_google_ads_languages", {}, async (_params, client) => {
        const response = await apiClient.get("/keywords_data/google_ads/languages");
        return response;
    }, apiClient);
    // Google Ads Keywords Categories
    (0, tools_js_1.registerTool)(server, "keywords_google_ads_categories", {}, async (_params, client) => {
        const response = await apiClient.get("/keywords_data/google_ads/categories");
        return response;
    }, apiClient);
    // Google Trends
    (0, tools_js_1.registerTool)(server, "keywords_google_trends_explore", {
        keywords: zod_1.z.array(zod_1.z.string()).describe("Keywords to explore"),
        location_code: zod_1.z.number().optional().describe("The location code for the search"),
        language_code: zod_1.z.string().optional().describe("The language code for the search"),
        date_from: zod_1.z.string().optional().describe("Start date in YYYY-MM-DD format"),
        date_to: zod_1.z.string().optional().describe("End date in YYYY-MM-DD format"),
        category_code: zod_1.z.number().optional().describe("Google Trends category code")
    }, async (params, client) => {
        const response = await apiClient.post("/keywords_data/google_trends/explore/live", [params]);
        return response;
    }, apiClient);
    // Bing Keyword Data
    (0, tools_js_1.registerTool)(server, "keywords_bing_keywords_for_keywords", {
        keyword: zod_1.z.string().describe("Keyword to get data for"),
        location_code: zod_1.z.number().optional().describe("The location code for the search"),
        language_code: zod_1.z.string().optional().describe("The language code for the search"),
    }, async (params, client) => {
        const response = await apiClient.post("/keywords_data/bing/keywords_for_keywords/live", [params]);
        return response;
    }, apiClient);
}
//# sourceMappingURL=index.js.map