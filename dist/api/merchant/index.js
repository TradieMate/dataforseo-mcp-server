"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.registerMerchantTools = registerMerchantTools;
const zod_1 = require("zod");
const tools_js_1 = require("../tools.js");
function registerMerchantTools(server, apiClient) {
    // Merchant Google Search
    (0, tools_js_1.registerTool)(server, "merchant_google_search", {
        keyword: zod_1.z.string().describe("Product name or related keyword"),
        location_name: zod_1.z.string().optional().describe("Location name"),
        location_code: zod_1.z.number().optional().describe("Location code"),
        language_name: zod_1.z.string().optional().describe("Language name"),
        language_code: zod_1.z.string().optional().describe("Language code"),
        depth: zod_1.z.number().optional().describe("Number of results to return"),
        limit: zod_1.z.number().optional().describe("Maximum number of results to return per page"),
        offset: zod_1.z.number().optional().describe("Offset for pagination")
    }, async (params, client) => {
        const response = await apiClient.post("/merchant/google/search/live", [params]);
        return response;
    }, apiClient);
    // Merchant Google Product Specs
    (0, tools_js_1.registerTool)(server, "merchant_google_product_specs", {
        product_id: zod_1.z.string().describe("Google Shopping Product ID"),
        location_name: zod_1.z.string().optional().describe("Location name"),
        location_code: zod_1.z.number().optional().describe("Location code"),
        language_name: zod_1.z.string().optional().describe("Language name"),
        language_code: zod_1.z.string().optional().describe("Language code")
    }, async (params, client) => {
        const response = await apiClient.post("/merchant/google/product_specs/live", [params]);
        return response;
    }, apiClient);
    // Merchant Google Product Info
    (0, tools_js_1.registerTool)(server, "merchant_google_product_info", {
        product_id: zod_1.z.string().describe("Google Shopping Product ID"),
        location_name: zod_1.z.string().optional().describe("Location name"),
        location_code: zod_1.z.number().optional().describe("Location code"),
        language_name: zod_1.z.string().optional().describe("Language name"),
        language_code: zod_1.z.string().optional().describe("Language code")
    }, async (params, client) => {
        const response = await apiClient.post("/merchant/google/product_info/live", [params]);
        return response;
    }, apiClient);
    // Merchant Google Sellers
    (0, tools_js_1.registerTool)(server, "merchant_google_sellers", {
        product_id: zod_1.z.string().describe("Google Shopping Product ID"),
        location_name: zod_1.z.string().optional().describe("Location name"),
        location_code: zod_1.z.number().optional().describe("Location code"),
        language_name: zod_1.z.string().optional().describe("Language name"),
        language_code: zod_1.z.string().optional().describe("Language code")
    }, async (params, client) => {
        const response = await apiClient.post("/merchant/google/sellers/live", [params]);
        return response;
    }, apiClient);
    // Merchant Google Reviews
    (0, tools_js_1.registerTool)(server, "merchant_google_reviews", {
        product_id: zod_1.z.string().describe("Google Shopping Product ID"),
        location_name: zod_1.z.string().optional().describe("Location name"),
        location_code: zod_1.z.number().optional().describe("Location code"),
        language_name: zod_1.z.string().optional().describe("Language name"),
        language_code: zod_1.z.string().optional().describe("Language code"),
        depth: zod_1.z.number().optional().describe("Number of reviews to retrieve"),
        offset: zod_1.z.number().optional().describe("Offset for pagination")
    }, async (params, client) => {
        const response = await apiClient.post("/merchant/google/reviews/live", [params]);
        return response;
    }, apiClient);
    // Merchant Google Locations
    (0, tools_js_1.registerTool)(server, "merchant_google_locations", {
        country: zod_1.z.string().optional().describe("Filter locations by country name")
    }, async (params) => {
        const url = params.country
            ? `/merchant/google/locations?country=${encodeURIComponent(params.country)}`
            : "/merchant/google/locations";
        const response = await apiClient.get(url);
        return response;
    }, apiClient);
    // Merchant Google Languages
    (0, tools_js_1.registerTool)(server, "merchant_google_languages", {}, async (_params, client) => {
        const response = await apiClient.get("/merchant/google/languages");
        return response;
    }, apiClient);
    // Merchant Amazon Search
    (0, tools_js_1.registerTool)(server, "merchant_amazon_search", {
        keyword: zod_1.z.string().describe("Product name or related keyword"),
        location_name: zod_1.z.string().optional().describe("Location name"),
        location_code: zod_1.z.number().optional().describe("Location code"),
        language_name: zod_1.z.string().optional().describe("Language name"),
        language_code: zod_1.z.string().optional().describe("Language code"),
        depth: zod_1.z.number().optional().describe("Number of results to return"),
        limit: zod_1.z.number().optional().describe("Maximum number of results to return per page"),
        offset: zod_1.z.number().optional().describe("Offset for pagination")
    }, async (params, client) => {
        const response = await apiClient.post("/merchant/amazon/search/live", [params]);
        return response;
    }, apiClient);
    // Merchant Amazon Product Info
    (0, tools_js_1.registerTool)(server, "merchant_amazon_product_info", {
        asin: zod_1.z.string().describe("Amazon ASIN"),
        location_name: zod_1.z.string().optional().describe("Location name"),
        location_code: zod_1.z.number().optional().describe("Location code"),
        language_name: zod_1.z.string().optional().describe("Language name"),
        language_code: zod_1.z.string().optional().describe("Language code")
    }, async (params, client) => {
        const response = await apiClient.post("/merchant/amazon/product_info/live", [params]);
        return response;
    }, apiClient);
    // Merchant Amazon Reviews
    (0, tools_js_1.registerTool)(server, "merchant_amazon_reviews", {
        asin: zod_1.z.string().describe("Amazon ASIN"),
        location_name: zod_1.z.string().optional().describe("Location name"),
        location_code: zod_1.z.number().optional().describe("Location code"),
        language_name: zod_1.z.string().optional().describe("Language name"),
        language_code: zod_1.z.string().optional().describe("Language code"),
        depth: zod_1.z.number().optional().describe("Number of reviews to retrieve"),
        offset: zod_1.z.number().optional().describe("Offset for pagination")
    }, async (params, client) => {
        const response = await apiClient.post("/merchant/amazon/reviews/live", [params]);
        return response;
    }, apiClient);
    // Merchant Amazon Locations
    (0, tools_js_1.registerTool)(server, "merchant_amazon_locations", {
        country: zod_1.z.string().optional().describe("Filter locations by country name")
    }, async (params) => {
        const url = params.country
            ? `/merchant/amazon/locations?country=${encodeURIComponent(params.country)}`
            : "/merchant/amazon/locations";
        const response = await apiClient.get(url);
        return response;
    }, apiClient);
    // Merchant Amazon Languages
    (0, tools_js_1.registerTool)(server, "merchant_amazon_languages", {}, async (_params, client) => {
        const response = await apiClient.get("/merchant/amazon/languages");
        return response;
    }, apiClient);
}
//# sourceMappingURL=index.js.map