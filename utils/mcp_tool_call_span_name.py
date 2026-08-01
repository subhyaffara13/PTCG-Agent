
def mcp_tool_call_span_name(data: "MCPToolCallSpanData") -> str:
    """``"{mcp.method.name} {tool}"`` e.g. ``"tools/call get-weather"`` (MCP semconv)."""
    return f"{data.method} {data.tool_name}".strip()

