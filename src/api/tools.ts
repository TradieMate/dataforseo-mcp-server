import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { DataForSeoClient } from "./client.js";

/**
 * Base helper function to register an MCP tool for DataForSEO API
 */
export function registerTool<T extends Record<string, z.ZodTypeAny>>(
  server: McpServer,
  name: string,
  schema: T,
  handler: (params: z.infer<z.ZodObject<T>>, client: DataForSeoClient) => Promise<any>,
  apiClient: DataForSeoClient
) {
  server.tool(
    name,
    schema,
    async (params) => {
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
      } catch (error) {
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
    }
  );
}

/**
 * Helper for registering a task-based tool (POST, READY, GET pattern)
 */
export function registerTaskTool<PostT extends Record<string, z.ZodTypeAny>>(
  server: McpServer,
  baseName: string,
  postSchema: PostT,
  postHandler: (params: z.infer<z.ZodObject<PostT>>, client: DataForSeoClient) => Promise<any>,
  readyHandler: (client: DataForSeoClient) => Promise<any>,
  getHandler: (id: string, client: DataForSeoClient) => Promise<any>,
  apiClient: DataForSeoClient
) {
  // Register POST tool
  registerTool(
    server,
    `${baseName}_post`,
    postSchema,
    postHandler,
    apiClient
  );
  
  // Register READY tool
  registerTool(
    server,
    `${baseName}_ready`,
    {},
    (_params, client) => readyHandler(client),
    apiClient
  );
  
  // Register GET tool
  registerTool(
    server,
    `${baseName}_get`,
    { id: z.string() },
    (params, client) => getHandler(params.id, client),
    apiClient
  );
}