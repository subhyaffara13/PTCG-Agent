from typing import Optional

def _resolve_oauth2_server_for_root_endpoints(
    client_ip: Optional[str] = None,
) -> Optional[MCPServer]:
    """
    Resolve the MCP server for root-level OAuth endpoints (no server name in path).

    When the MCP SDK hits root-level endpoints like /register, /authorize, /token
    without a server name prefix, we try to find the right server automatically.
    Returns the server if exactly one OAuth2 server is configured, else None.
    """
    from litellm.proxy._experimental.mcp_server.mcp_server_manager import (
        global_mcp_server_manager,
    )

    registry = global_mcp_server_manager.get_filtered_registry(client_ip=client_ip)
    oauth2_servers = [s for s in registry.values() if s.auth_type == MCPAuth.oauth2]
    if len(oauth2_servers) == 1:
        return oauth2_servers[0]
    return None

