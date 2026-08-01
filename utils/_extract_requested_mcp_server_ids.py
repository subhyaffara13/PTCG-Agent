
def _extract_requested_mcp_server_ids(
    object_permission: Optional[dict],
) -> Set[str]:
    """
    Extract all MCP server IDs referenced in a key's object_permission dict.

    Includes:
    - mcp_servers list
    - Keys from mcp_tool_permissions
    """
    if not object_permission or not isinstance(object_permission, dict):
        return set()

    server_ids: Set[str] = set()
    mcp_servers = object_permission.get("mcp_servers")
    if isinstance(mcp_servers, list):
        server_ids.update(mcp_servers)

    mcp_tool_permissions = object_permission.get("mcp_tool_permissions")
    if isinstance(mcp_tool_permissions, dict):
        server_ids.update(mcp_tool_permissions.keys())

    return server_ids

