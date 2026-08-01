
def _iter_inspection_messages(data: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
    """Yield every message-like dict, walking ``messages`` AND ``input``."""
    messages = data.get("messages")
    if isinstance(messages, list):
        yield from messages
    yield from _coerce_input_to_messages(data.get("input"))

