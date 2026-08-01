
def _coerce_input_to_messages(input_value: Any) -> List[Dict[str, Any]]:
    """Coerce a Responses-API ``data["input"]`` value into chat-style messages."""
    if isinstance(input_value, str):
        return [{"role": "user", "content": input_value}]
    if isinstance(input_value, list):
        if input_value and all(
            isinstance(item, dict) and "role" in item for item in input_value
        ):
            return list(input_value)
        # Mixed lists (content-part dicts + bare strings) and pure
        # string/dict lists all become a single user message; the content
        # iterator below handles each element type uniformly.
        return [{"role": "user", "content": input_value}]
    return []

