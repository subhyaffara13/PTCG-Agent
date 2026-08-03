from typing import Any, Tuple

def _extract_tool_call_fields(tool_call: Any, fallback_call_id: str) -> Tuple[str, str]:
    """Extract (call_id, raw_arguments_string) from a dict or Pydantic tool_call item."""
    if isinstance(tool_call, dict):
        call_id = str(
            tool_call.get("call_id") or tool_call.get("id") or fallback_call_id
        )
        raw_args = tool_call.get("arguments") or "{}"
    else:
        raw_call_id = (
            getattr(tool_call, "call_id", None)
            or getattr(tool_call, "id", None)
            or fallback_call_id
        )
        call_id = str(raw_call_id)
        raw_args = getattr(tool_call, "arguments", "{}") or "{}"
    return call_id, raw_args

