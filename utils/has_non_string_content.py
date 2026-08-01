
def has_non_string_content(data: Dict[str, Any]) -> bool:
    """Return True if any inspected content is not a plain string.

    Used by hooks whose mask/redact path operates on string offsets and
    therefore cannot preserve multimodal non-text parts. Such hooks should
    degrade to block-on-detect when this returns True so image/audio parts
    are not silently stripped during in-place masking.
    """
    messages = data.get("messages")
    if isinstance(messages, list):
        for message in messages:
            if isinstance(message, dict) and not isinstance(
                message.get("content"), str
            ):
                if message.get("content") is not None:
                    return True
    input_value = data.get("input")
    if input_value is not None and not isinstance(input_value, str):
        return True
    return False

