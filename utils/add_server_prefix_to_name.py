
def add_server_prefix_to_name(name: str, server_name: str) -> str:
    """Add server name prefix to any MCP resource name."""
    formatted_server_name = normalize_server_name(server_name)

    return MCP_TOOL_PREFIX_FORMAT.format(
        server_name=formatted_server_name,
        separator=MCP_TOOL_PREFIX_SEPARATOR,
        tool_name=name,
    )

