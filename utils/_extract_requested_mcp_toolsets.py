
def _extract_requested_mcp_toolsets(
    object_permission: Optional[dict],
) -> Set[str]:
    """Extract MCP toolset IDs from a key's object_permission dict."""
    if not object_permission or not isinstance(object_permission, dict):
        return set()

    toolsets = object_permission.get("mcp_toolsets")
    if isinstance(toolsets, list):
        return set(toolsets)
    return set()

