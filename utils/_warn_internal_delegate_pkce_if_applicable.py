
def _warn_internal_delegate_pkce_if_applicable(
    server: MCPServer, *, source: str
) -> None:
    """Surface internal + upstream PKCE delegate in logs for operators."""
    if server.auth_type != MCPAuth.oauth2:
        return
    if getattr(server, "delegate_auth_to_upstream", False) is not True:
        return
    if getattr(server, "available_on_public_internet", True):
        return
    if server.has_client_credentials:
        return
    label = get_server_prefix(server)
    verbose_logger.warning(
        "MCP server %r (id=%s, source=%s): internal-only (available_on_public_internet=false) "
        "with delegate_auth_to_upstream=true. Anonymous callers can reach the upstream OAuth2 "
        "/authorize flow and complete PKCE without a LiteLLM API key session; ensure the "
        "upstream IdP and network enforce your access policy.",
        label,
        server.server_id,
        source,
    )

