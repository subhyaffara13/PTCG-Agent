import json
from typing import Any, Optional

def _input_snippet_for_log(sl: Any) -> Optional[str]:
    """Snippet for request input: prefer messages, fall back to proxy_server_request (same as drawer)."""
    out = _snippet(sl.messages)
    if out:
        return out
    psr = getattr(sl, "proxy_server_request", None)
    if not psr:
        return None
    if isinstance(psr, str):
        try:
            psr = json.loads(psr)
        except Exception:
            return _snippet(psr)
    if isinstance(psr, dict):
        msgs = psr.get("messages")
        if msgs is None and isinstance(psr.get("body"), dict):
            msgs = psr["body"].get("messages")
        out = _snippet(msgs)
        if out:
            return out
        return _snippet(psr)
    return _snippet(psr)

