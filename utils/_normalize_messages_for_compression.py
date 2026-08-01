
def _normalize_messages_for_compression(
    messages: List[dict],
    call_type: str,
) -> Tuple[List[dict], List[dict]]:
    """
    Normalize each original message to a text-surrogate content for scoring.

    Returns:
        (normalized_messages, original_messages_copy)
    """
    if call_type not in _SUPPORTED_CALL_TYPES:
        raise ValueError(
            f"Unsupported call_type={call_type!r} for compression. "
            f"Expected one of: {sorted(_SUPPORTED_CALL_TYPES)}."
        )

    original_messages: List[Dict[str, Any]] = [dict(m) for m in messages]

    normalized_messages: List[dict] = []
    for msg in original_messages:
        normalized_messages.append(
            {
                **msg,
                "content": _content_to_text(msg.get("content", "")),
            }
        )
    return normalized_messages, original_messages

