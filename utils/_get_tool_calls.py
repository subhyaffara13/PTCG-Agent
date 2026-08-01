
def _get_tool_calls(message) -> Optional[list]:
    """Return ``message.tool_calls`` only when it's a non-empty list.

    Works for dicts and Pydantic message objects via ``_safe_get``.
    """
    tool_calls = _safe_get(message, "tool_calls")
    return tool_calls if isinstance(tool_calls, list) and tool_calls else None

