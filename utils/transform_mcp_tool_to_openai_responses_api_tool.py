
def transform_mcp_tool_to_openai_responses_api_tool(
    mcp_tool: MCPTool,
) -> FunctionToolParam:
    """Convert an MCP tool to an OpenAI Responses API tool."""
    normalized_parameters = _normalize_mcp_input_schema(mcp_tool.inputSchema)

    return FunctionToolParam(
        name=mcp_tool.name,
        parameters=normalized_parameters,
        strict=False,
        type="function",
        description=mcp_tool.description or "",
    )

