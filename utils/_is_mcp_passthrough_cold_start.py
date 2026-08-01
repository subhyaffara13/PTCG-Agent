
def _is_mcp_passthrough_cold_start(
    mcp_servers: Optional[List[str]], client_ip: Optional[str]
) -> bool:
    """True only when EVERY targeted server is a pass-through server with no
    auth headers — the cold-start OAuth discovery case per RFC 9728 / MCP
    Authorization spec. Lets the route handler's 401 emitter produce the
    spec-compliant WWW-Authenticate challenge instead of surfacing a generic
    admission error.

    Uses "all" semantics (mirrors
    :meth:`MCPRequestHandler._target_servers_delegate_auth_to_upstream`): one
    non-passthrough target in a co-targeted set must not flip the bypass open
    for the others. Fails closed when any target cannot be resolved."""
    if not mcp_servers:
        return False
    from litellm.proxy._experimental.mcp_server.mcp_server_manager import (
        global_mcp_server_manager,
    )

    for name in mcp_servers:
        server = global_mcp_server_manager.get_mcp_server_by_name(
            name, client_ip=client_ip
        )
        if server is None or not getattr(server, "is_oauth_passthrough", False):
            return False
    return True

