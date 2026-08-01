
def _extract_model_from_first_ws_event(first_event: Any) -> Optional[str]:
    """Extract model from a response.create WS event, handling flat and nested formats.

    Flat:   {"type": "response.create", "model": "gpt-4o", ...}
    Nested: {"type": "response.create", "response": {"model": "gpt-4o", ...}}
    """
    if not isinstance(first_event, dict):
        return None
    nested = first_event.get("response")
    return (
        nested.get("model") if isinstance(nested, dict) else None
    ) or first_event.get("model")

