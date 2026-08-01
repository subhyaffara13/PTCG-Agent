
def _mcp_session_id_from_headers(
    raw_headers: Optional[Dict[str, str]],
) -> Optional[str]:
    """The ``mcp-session-id`` of a stateful MCP session, read case-insensitively
    from the request headers. ``None`` for stateless calls (no such header)."""
    if not raw_headers:
        return None
    for key, value in raw_headers.items():
        if isinstance(key, str) and key.lower() == "mcp-session-id":
            return value or None
    return None

