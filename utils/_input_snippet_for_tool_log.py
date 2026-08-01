
def _input_snippet_for_tool_log(sl: Any, max_len: int = 200) -> Optional[str]:
    """Short snippet from messages or proxy_server_request for tool usage log row."""
    if sl is None:
        return None
    messages = getattr(sl, "messages", None)
    if messages is not None:
        s = _snippet_str(messages, max_len)
        if s:
            return s
    psr = getattr(sl, "proxy_server_request", None)
    if not psr:
        return None
    if isinstance(psr, str):
        import json

        try:
            psr = json.loads(psr)
        except Exception:
            return _snippet_str(psr, max_len)
    if isinstance(psr, dict):
        msgs = psr.get("messages")
        if msgs is None and isinstance(psr.get("body"), dict):
            msgs = psr["body"].get("messages")
        s = _snippet_str(msgs, max_len)
        if s:
            return s
    return _snippet_str(psr, max_len)

