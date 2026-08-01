
def _create_elicitation_callback():
    """
    Create an elicitation callback for MCP ClientSession.
    Returns a callable that handles elicitation/create requests from
    upstream MCP servers. In gateway mode, this relays to the downstream
    client; in tool bridge mode, it returns a decline response.
    """
    if not MCP_ELICITATION_AVAILABLE:
        return None

    async def _elicitation_callback(context, params):
        from litellm.proxy._experimental.mcp_server.elicitation_handler import (
            handle_elicitation_request,
        )
        from litellm.proxy._experimental.mcp_server.server import get_active_mcp_session

        # In Gateway mode, we relay the elicitation request to the downstream client
        # that triggered the current operation.
        downstream_session = get_active_mcp_session()
        downstream_capabilities = (
            getattr(downstream_session, "capabilities", None)
            if downstream_session
            else None
        )

        return await handle_elicitation_request(
            context=context,
            params=params,
            downstream_session=downstream_session,
            downstream_capabilities=downstream_capabilities,
        )

    return _elicitation_callback

