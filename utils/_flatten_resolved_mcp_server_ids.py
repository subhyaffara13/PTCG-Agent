
def _flatten_resolved_mcp_server_ids(
    identifier_to_server_ids: Dict[str, Set[str]],
) -> Set[str]:
    return {
        server_id
        for server_ids in identifier_to_server_ids.values()
        for server_id in server_ids
    }

