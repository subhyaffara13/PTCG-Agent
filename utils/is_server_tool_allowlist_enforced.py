
def is_server_tool_allowlist_enforced(mcp_server: Any) -> bool:
    mcp_info = _parse_mcp_info_dict(getattr(mcp_server, "mcp_info", None))
    if not mcp_info:
        return False
    return bool(mcp_info.get(MCP_TOOL_ALLOWLIST_ENFORCED_KEY))

