from typing import Any, Dict

def iter_message_text(data: Dict[str, Any]) -> Iterator[str]:
    """Yield every text fragment from ``messages`` AND ``input``.

    Walks every role (user, assistant, system, …) — guardrails inspect
    the entire conversation, not just user turns.
    """
    for message in _iter_inspection_messages(data):
        if not isinstance(message, dict):
            continue
        yield from _iter_text_parts_in_content(message.get("content"))

