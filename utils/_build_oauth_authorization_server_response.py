from typing import Optional

def _build_oauth_authorization_server_response(
    request: Request,
    mcp_server_name: Optional[str],
) -> dict:
    """Build OAuth authorization server metadata response (gateway-as-AS shape).

    Synchronous because the body only does dict construction and synchronous
    registry lookups; unlike :func:`_build_oauth_protected_resource_response`
    it does not need to await any upstream IO.
    """
    from litellm.proxy._experimental.mcp_server.mcp_server_manager import (
        global_mcp_server_manager,
    )

    request_base_url = get_request_base_url(request)
    client_ip = IPAddressUtils.get_mcp_client_ip(request)

    # When no server name provided, try to resolve the single OAuth2 server
    if mcp_server_name is None:
        resolved = _resolve_oauth2_server_for_root_endpoints(client_ip=client_ip)
        if resolved:
            mcp_server_name = resolved.server_name or resolved.name

    authorization_endpoint = (
        f"{request_base_url}/{mcp_server_name}/authorize"
        if mcp_server_name
        else f"{request_base_url}/authorize"
    )
    token_endpoint = (
        f"{request_base_url}/{mcp_server_name}/token"
        if mcp_server_name
        else f"{request_base_url}/token"
    )

    mcp_server: Optional[MCPServer] = None
    if mcp_server_name:
        mcp_server = global_mcp_server_manager.get_mcp_server_by_name(
            mcp_server_name, client_ip=client_ip
        )

    return {
        "issuer": request_base_url,  # point to your proxy
        "authorization_endpoint": authorization_endpoint,
        "token_endpoint": token_endpoint,
        "response_types_supported": ["code"],
        "scopes_supported": (
            mcp_server.scopes if mcp_server and mcp_server.scopes else []
        ),
        "grant_types_supported": ["authorization_code", "refresh_token"],
        "code_challenge_methods_supported": ["S256"],
        "token_endpoint_auth_methods_supported": ["client_secret_post"],
        # Claude expects a registration endpoint, even if we just fake it
        "registration_endpoint": (
            f"{request_base_url}/{mcp_server_name}/register"
            if mcp_server_name
            else f"{request_base_url}/register"
        ),
    }

