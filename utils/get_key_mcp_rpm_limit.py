from typing import Dict, Optional

def get_key_mcp_rpm_limit(
    user_api_key_dict: UserAPIKeyAuth,
) -> Optional[Dict[str, int]]:
    """
    Get the per-MCP-server rpm limit for a given api key.

    Priority order (returns first found):
    1. Key metadata (mcp_rpm_limit)
    2. Team metadata (mcp_rpm_limit)

    The returned dict is keyed by MCP server name (alias if set, else the
    configured server name).
    """
    if user_api_key_dict.metadata:
        result = user_api_key_dict.metadata.get("mcp_rpm_limit")
        if result is not None:
            return result

    if user_api_key_dict.team_metadata:
        team_limit = user_api_key_dict.team_metadata.get("mcp_rpm_limit")
        if team_limit is not None:
            return team_limit

    return None

