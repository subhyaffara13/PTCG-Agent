
def _resolve_tool_names_from_messages(messages: List[dict]) -> Dict[str, str]:
    """
    Build a map of tool_call_id -> tool_name from assistant messages' tool_calls.
    Used to resolve which tool produced each tool result in the conversation.
    """
    mapping: Dict[str, str] = {}
    for msg in messages:
        if msg.get("role") != "assistant":
            continue
        tool_calls = msg.get("tool_calls") or []
        for tc in tool_calls:
            if isinstance(tc, dict):
                tc_id = tc.get("id")
                fn = (tc.get("function") or {}).get("name")
            else:
                tc_id = getattr(tc, "id", None)
                fn_obj = getattr(tc, "function", None)
                fn = getattr(fn_obj, "name", None) if fn_obj else None
            if tc_id and fn:
                mapping[tc_id] = fn
    return mapping

