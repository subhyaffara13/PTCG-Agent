from typing import List, Optional

def _parse_mcp_server_names_from_path(
    path: str, mcp_servers_header: Optional[List[str]] = None
) -> Optional[List[str]]:
    """Resolve the single MCP server name a cold-start passthrough bypass may
    target. Delegates parsing to
    :meth:`MCPRequestHandler._extract_target_server_names_from_path` so the
    names used here always match the names downstream routing uses; returns
    ``None`` whenever the bypass must not activate (aggregate ``/mcp``,
    multi-server CSV paths, or any other unrecognized path).

    Also fails closed when the ``x-mcp-servers`` header introduces any server
    not present in the path-derived target set. Downstream routing for
    ``/mcp/...`` paths overrides the header with path-derived names, but a
    header/path mismatch here is a sign of a confused or hostile caller —
    refuse the cold-start bypass rather than admit anonymously based on the
    path while the header advertises a stricter, non-passthrough target."""
    servers = MCPRequestHandler._extract_target_server_names_from_path(path)
    if len(servers) != 1:
        verbose_logger.debug(
            "MCP cold-start: path %r resolved to %r; passthrough 401 bypass "
            "requires exactly one target and will not activate",
            path,
            servers,
        )
        return None
    if mcp_servers_header is not None and (set(mcp_servers_header) - set(servers)):
        verbose_logger.debug(
            "MCP cold-start: x-mcp-servers header %r introduces target(s) not "
            "in path-derived set %r; passthrough 401 bypass will not activate",
            mcp_servers_header,
            servers,
        )
        return None
    return servers

