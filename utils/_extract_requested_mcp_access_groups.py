from typing import Optional, Set

def _extract_requested_mcp_access_groups(
    object_permission: Optional[dict],
) -> Set[str]:
    """Extract MCP access groups from a key's object_permission dict."""
    if not object_permission or not isinstance(object_permission, dict):
        return set()

    groups = object_permission.get("mcp_access_groups")
    if isinstance(groups, list):
        return set(groups)
    return set()

