
def get_server_prefix(server: Any) -> str:
    """Return the prefix for a server.

    When the short-prefix mode is enabled (``LITELLM_USE_SHORT_MCP_TOOL_PREFIX``)
    a three-character base62 ID is returned.  We prefer the cached
    ``server.short_prefix`` value when set — that field is populated at
    registration time by ``MCPServerManager._assign_unique_short_prefix``
    and resolves natural-hash collisions deterministically — and only fall
    back to the natural hash for ad-hoc / temp-server objects without a
    cached value.  In default mode the historical behaviour is preserved:
    alias if present, else server_name, else server_id.
    """
    if is_short_mcp_tool_prefix_enabled():
        cached = getattr(server, "short_prefix", None)
        if cached:
            return cached
        server_id = getattr(server, "server_id", None)
        if server_id:
            return compute_short_server_prefix(server_id)

    if hasattr(server, "alias") and server.alias:
        return server.alias
    if hasattr(server, "server_name") and server.server_name:
        return server.server_name
    if hasattr(server, "server_id"):
        return server.server_id
    return ""

