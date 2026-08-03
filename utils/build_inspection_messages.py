from typing import Any, Dict, List

def build_inspection_messages(data: Dict[str, Any]) -> List[Dict[str, str]]:
    """Synthesize a chat-style messages list for posting to a guardrail API.

    Each returned message has a plain-string ``content`` — multimodal text
    parts are joined with newlines and Responses-API ``input`` is lifted
    into synthetic messages. Messages with no inspectable text are dropped.

    Hooks that POST ``{"messages": [...]}`` to an external service should
    call this instead of ``data.get("messages", [])`` so the Responses API
    and multimodal content are covered.
    """
    flattened: List[Dict[str, str]] = []
    for message in _iter_inspection_messages(data):
        if not isinstance(message, dict):
            continue
        text = "\n".join(_iter_text_parts_in_content(message.get("content")))
        if not text:
            continue
        role = message.get("role", "user") or "user"
        flattened.append({"role": role, "content": text})
    return flattened

