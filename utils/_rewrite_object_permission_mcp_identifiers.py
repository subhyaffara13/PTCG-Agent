
def _rewrite_object_permission_mcp_identifiers(
    object_permission: Optional[dict],
    identifier_to_server_ids: Dict[str, Set[str]],
) -> None:
    if not object_permission or not isinstance(object_permission, dict):
        return

    _rewrite_object_permission_mcp_servers(
        object_permission=object_permission,
        identifier_to_server_ids=identifier_to_server_ids,
    )
    _rewrite_object_permission_mcp_tool_permissions(
        object_permission=object_permission,
        identifier_to_server_ids=identifier_to_server_ids,
    )

