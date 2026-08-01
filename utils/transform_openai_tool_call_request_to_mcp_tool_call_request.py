
def transform_openai_tool_call_request_to_mcp_tool_call_request(
    openai_tool: Union[ChatCompletionMessageToolCall, Dict],
) -> MCPCallToolRequestParams:
    """Convert an OpenAI ChatCompletionMessageToolCall to an MCP CallToolRequestParams."""
    function = openai_tool["function"]
    return MCPCallToolRequestParams(
        name=function["name"],
        arguments=_get_function_arguments(function),
    )

