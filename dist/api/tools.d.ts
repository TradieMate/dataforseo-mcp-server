import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { DataForSeoClient } from "./client.js";
/**
 * Base helper function to register an MCP tool for DataForSEO API
 */
export declare function registerTool<T extends Record<string, z.ZodTypeAny>>(server: McpServer, name: string, schema: T, handler: (params: any, client: DataForSeoClient) => Promise<any>, apiClient: DataForSeoClient): void;
/**
 * Helper for registering a task-based tool (POST, READY, GET pattern)
 */
export declare function registerTaskTool<PostT extends Record<string, z.ZodTypeAny>>(server: McpServer, baseName: string, postSchema: PostT, postHandler: (params: any, client: DataForSeoClient) => Promise<any>, readyHandler: (client: DataForSeoClient) => Promise<any>, getHandler: (id: string, client: DataForSeoClient) => Promise<any>, apiClient: DataForSeoClient): void;
