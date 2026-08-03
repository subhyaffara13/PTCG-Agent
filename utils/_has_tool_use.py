from typing import Any

def _has_tool_use(content: Any) -> bool:
    """Check if content contains ToolUseContent."""
    if isinstance(content, list):
        return any(getattr(c, "type", None) == "tool_use" for c in content)
    return getattr(content, "type", None) == "tool_use"

