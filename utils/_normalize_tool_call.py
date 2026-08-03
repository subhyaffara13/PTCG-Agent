import json
from typing import Any, Dict, Optional

def _normalize_tool_call(tool_call: dict) -> dict:
    """Normalize a parsed tool call to ``{"name": str, "arguments": str}``.

    Different models return different structures from ``parse_response``:
    - Gemma: ``{"function": {"name": ..., "arguments": {...}}}`` (nested, arguments as dict)
    - Qwen:  ``{"name": ..., "arguments": {...}}`` (flat, arguments as dict)

    The OpenAI API expects ``arguments`` as a JSON **string**, so we ``json.dumps`` it.
    """
    function = tool_call.get("function", tool_call)
    arguments = function.get("arguments", {})
    return {
        "name": function["name"],
        "arguments": json.dumps(arguments) if not isinstance(arguments, str) else arguments,
    }


def _normalize_tool_call(raw_tc) -> Optional[Dict[str, Any]]:
    """Normalize a single tool_call (dict or Pydantic) into a stable shape:

        {"id": str|None, "type": str, "function": {"name": str|None, "arguments": str|None}}

    Arguments are coerced to a JSON string per OpenInference convention.
    Returns ``None`` when ``raw_tc`` cannot be coerced to a dict.
    """
    tc = _to_plain_dict(raw_tc)
    if not isinstance(tc, dict):
        return None
    function = _to_plain_dict(tc.get("function"))
    name = function.get("name") if isinstance(function, dict) else None
    args = function.get("arguments") if isinstance(function, dict) else None
    if args is not None and not isinstance(args, str):
        try:
            args = json.dumps(args)
        except Exception:
            args = str(args)
    return {
        "id": tc.get("id"),
        "type": tc.get("type", "function"),
        "function": {"name": name, "arguments": args},
    }

