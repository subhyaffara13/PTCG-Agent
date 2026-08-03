from typing import Any, Dict, List

def get_tools_for_role(is_admin: bool) -> List[Dict[str, Any]]:
    """Return the tool list appropriate for the user's role."""
    return TOOLS_ADMIN if is_admin else TOOLS_BASE

