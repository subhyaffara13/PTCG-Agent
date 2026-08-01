
def _has_client_supplied_mcp_auth(
    mcp_auth_header: Optional[str],
    mcp_server_auth_headers: Optional[Dict[str, Dict[str, str]]],
) -> bool:
    return bool(mcp_auth_header) or bool(mcp_server_auth_headers)

