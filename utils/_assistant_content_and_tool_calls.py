from typing import Any, Dict, List

def _assistant_content_and_tool_calls(response_obj: Any) -> tuple:
    """Return (assistant_text, tool_calls_list) extracted from a ModelResponse-ish object."""
    if response_obj is None:
        return None, []
    try:
        choices = getattr(response_obj, "choices", None) or response_obj.get("choices")
    except Exception:
        return None, []
    if not choices:
        return None, []

    msg = choices[0]
    msg = getattr(msg, "message", None) or (
        msg.get("message") if isinstance(msg, dict) else None
    )
    if msg is None:
        return None, []

    content = getattr(msg, "content", None)
    if content is None and isinstance(msg, dict):
        content = msg.get("content")

    raw_tool_calls = getattr(msg, "tool_calls", None)
    if raw_tool_calls is None and isinstance(msg, dict):
        raw_tool_calls = msg.get("tool_calls")
    tool_calls: List[Dict[str, Any]] = []
    for tc in raw_tool_calls or []:
        if isinstance(tc, dict):
            tool_calls.append(tc)
        else:
            try:
                tool_calls.append(tc.model_dump())
            except Exception:
                tool_calls.append({"name": getattr(tc, "name", ""), "arguments": ""})
    return content, tool_calls

