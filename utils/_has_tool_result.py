from typing import Any

def _has_tool_result(content: Any) -> bool:
    """Check if content contains ToolResultContent."""
    if isinstance(content, list):
        return any(getattr(c, "type", None) == "tool_result" for c in content)
    return getattr(content, "type", None) == "tool_result"

