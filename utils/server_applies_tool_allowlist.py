from typing import Any

def server_applies_tool_allowlist(mcp_server: Any) -> bool:
    """Whether server-level allowed_tools whitelist filtering is active."""
    allowed_tools = getattr(mcp_server, "allowed_tools", None) or []
    return is_server_tool_allowlist_enforced(mcp_server) or bool(allowed_tools)

