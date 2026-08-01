
def split_server_prefix_from_name(prefixed_name: str) -> Tuple[str, str]:
    """Return the unprefixed name plus the server name used as prefix."""
    if MCP_TOOL_PREFIX_SEPARATOR in prefixed_name:
        parts = prefixed_name.split(MCP_TOOL_PREFIX_SEPARATOR, 1)
        if len(parts) == 2:
            return parts[1], parts[0]
    return prefixed_name, ""

