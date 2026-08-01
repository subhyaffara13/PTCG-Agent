
def merge_mcp_headers(
    *,
    extra_headers: Optional[Mapping[str, str]] = None,
    static_headers: Optional[Mapping[str, str]] = None,
) -> Optional[Dict[str, str]]:
    """Merge outbound HTTP headers for MCP calls.

    This is used when calling out to external MCP servers (or OpenAPI-based MCP tools).

    Merge rules:
    - Start with `extra_headers` (typically OAuth2-derived headers)
    - Overlay `static_headers` (user-configured per MCP server)

    If both contain the same key, `static_headers` wins. This matches the existing
    behavior in `MCPServerManager` where `server.static_headers` is applied after
    any caller-provided headers.
    """
    merged: Dict[str, str] = {}

    if extra_headers:
        merged.update({str(k): str(v) for k, v in extra_headers.items()})

    if static_headers:
        merged.update({str(k): str(v) for k, v in static_headers.items()})

    return merged or None

