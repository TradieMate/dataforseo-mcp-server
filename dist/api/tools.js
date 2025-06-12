"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.registerTool = registerTool;
exports.registerTaskTool = registerTaskTool;
const zod_1 = require("zod");
/**
 * Base helper function to register an MCP tool for DataForSEO API
 */
function registerTool(server, name, schema, handler, apiClient) {
    server.tool(name, `DataForSEO API tool: ${name}`, async (params) => {
        try {
            const result = await handler(params, apiClient);
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify(result, null, 2)
                    }
                ]
            };
        }
        catch (error) {
            console.error(`Error in ${name} tool:`, error);
            if (error instanceof Error) {
                return {
                    content: [
                        {
                            type: "text",
                            text: JSON.stringify({
                                error: error.message,
                                stack: error.stack
                            }, null, 2)
                        }
                    ]
                };
            }
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify({
                            error: "Unknown error occurred",
                            details: error
                        }, null, 2)
                    }
                ]
            };
        }
    });
}
/**
 * Helper for registering a task-based tool (POST, READY, GET pattern)
 */
function registerTaskTool(server, baseName, postSchema, postHandler, readyHandler, getHandler, apiClient) {
    // Register POST tool
    registerTool(server, `${baseName}_post`, postSchema, postHandler, apiClient);
    // Register READY tool
    registerTool(server, `${baseName}_ready`, {}, (_params, client) => readyHandler(client), apiClient);
    // Register GET tool
    registerTool(server, `${baseName}_get`, { id: zod_1.z.string() }, (params, client) => getHandler(params.id, client), apiClient);
}
//# sourceMappingURL=tools.js.map