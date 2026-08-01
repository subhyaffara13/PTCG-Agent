
def _rewrite_object_permission_mcp_servers(
    object_permission: dict,
    identifier_to_server_ids: Dict[str, Set[str]],
) -> None:
    mcp_servers = object_permission.get("mcp_servers")
    if not isinstance(mcp_servers, list):
        return

    normalized_servers: List[str] = []
    for identifier in mcp_servers:
        normalized_servers.extend(sorted(identifier_to_server_ids.get(identifier, [])))
    object_permission["mcp_servers"] = _dedupe_preserving_order(normalized_servers)

