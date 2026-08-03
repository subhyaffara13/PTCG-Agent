from typing import Any, Dict, List

def _extract_tool_calls(content: Any) -> List[Dict[str, Any]]:
    """Extract OpenAI-format tool_calls from MCP ToolUseContent."""
    import json

    items = content if isinstance(content, list) else [content]
    tool_calls = []
    for item in items:
        if getattr(item, "type", None) == "tool_use":
            tool_calls.append(
                {
                    "id": getattr(item, "id", f"call_{id(item)}"),
                    "type": "function",
                    "function": {
                        "name": getattr(item, "name", ""),
                        "arguments": json.dumps(
                            getattr(item, "input", {}), default=str
                        ),
                    },
                }
            )
    return tool_calls

