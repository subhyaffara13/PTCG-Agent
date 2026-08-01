
def _create_sampling_callback(user_api_key_auth: Optional[Any] = None):
    """
    Create a sampling callback for MCP ClientSession.
    Returns a callable that handles sampling/createMessage requests from
    upstream MCP servers by routing them through litellm.acompletion().
    """
    if not MCP_SAMPLING_AVAILABLE:
        return None

    async def _sampling_callback(context, params):
        from litellm.proxy._experimental.mcp_server.sampling_handler import (
            handle_sampling_create_message,
        )
        import litellm
        from litellm.proxy._experimental.mcp_server.server import (
            get_active_auth_context,
        )

        auth_context = get_active_auth_context()
        resolved_auth = user_api_key_auth or (
            auth_context.user_api_key_auth if auth_context else None
        )
        # Forward original HTTP headers and client IP so that
        # header-dependent guardrails, tag-based routing, trace
        # correlation, and forward_llm_provider_auth_headers work
        # correctly for sampling sub-calls.
        _raw_headers = getattr(auth_context, "raw_headers", None)
        _client_ip = getattr(auth_context, "client_ip", None)

        return await handle_sampling_create_message(
            context=context,
            params=params,
            default_model=getattr(litellm, "default_mcp_sampling_model", None),
            user_api_key_auth=resolved_auth,
            raw_headers=_raw_headers,
            client_ip=_client_ip,
        )

    return _sampling_callback

