
def is_tool_name_prefixed(
    tool_name: str,
    known_server_prefixes: Optional[set] = None,
) -> bool:
    """
    Check if tool name has a known MCP server prefix.

    When ``known_server_prefixes`` is provided the function verifies that the
    substring before the first separator is an actual registered server
    prefix.  Without it the check falls back to the legacy heuristic
    (separator present anywhere in the name), which can produce false
    positives for non-MCP tools whose names contain hyphens
    (e.g. ``text-to-speech``, ``code-review``).

    Args:
        tool_name: Tool name to check.
        known_server_prefixes: Optional set of normalised server prefixes
            currently registered in the MCP manager.  Pass this whenever
            the caller has access to the server registry so that the check
            is accurate.

    Returns:
        True if tool name is prefixed, False otherwise.
    """
    if MCP_TOOL_PREFIX_SEPARATOR not in tool_name:
        return False

    if known_server_prefixes is not None:
        candidate_prefix = tool_name.split(MCP_TOOL_PREFIX_SEPARATOR, 1)[0]
        return normalize_server_name(candidate_prefix) in known_server_prefixes

    # Legacy fallback – separator present somewhere in the name.
    return True

