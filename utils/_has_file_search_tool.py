from typing import Any, Optional

def _has_file_search_tool(tools: Optional[Any]) -> bool:
    """Return True if any tool in the list has type 'file_search'."""
    if not tools:
        return False
    return any(isinstance(t, dict) and t.get("type") == "file_search" for t in tools)

