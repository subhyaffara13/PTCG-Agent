from typing import Set

def _get_allow_all_keys_server_ids() -> Set[str]:
    """Return the set of MCP server IDs marked with allow_all_keys=True."""
    from litellm.proxy._experimental.mcp_server.mcp_server_manager import (
        global_mcp_server_manager,
    )

    return set(global_mcp_server_manager.get_allow_all_keys_server_ids())

