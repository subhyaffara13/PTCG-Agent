import json
from typing import Any, Dict, Optional

def _parse_mcp_info_dict(mcp_info: Any) -> Optional[Dict[str, Any]]:
    if mcp_info is None:
        return None
    if isinstance(mcp_info, dict):
        return mcp_info
    if isinstance(mcp_info, str):
        try:
            parsed = json.loads(mcp_info)
        except (ValueError, TypeError):
            return None
        return parsed if isinstance(parsed, dict) else None
    return None

