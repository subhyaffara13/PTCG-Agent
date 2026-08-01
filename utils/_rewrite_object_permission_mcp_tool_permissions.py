
def _rewrite_object_permission_mcp_tool_permissions(
    object_permission: dict,
    identifier_to_server_ids: Dict[str, Set[str]],
) -> None:
    mcp_tool_permissions = object_permission.get("mcp_tool_permissions")
    if not isinstance(mcp_tool_permissions, dict):
        return

    normalized_tool_permissions: Dict[str, List[str]] = {}
    for identifier, tools in mcp_tool_permissions.items():
        if not isinstance(tools, list):
            tools = []
        for server_id in sorted(identifier_to_server_ids.get(identifier, [])):
            normalized_tool_permissions.setdefault(server_id, [])
            normalized_tool_permissions[server_id].extend(tools)

    object_permission["mcp_tool_permissions"] = {
        server_id: _dedupe_preserving_order(tools)
        for server_id, tools in normalized_tool_permissions.items()
    }

