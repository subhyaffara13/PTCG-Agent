
def sanitize_event_metadata(
    event_metadata: Mapping[str, object] | None,
) -> dict[str, str]:
    """Reduce caller-supplied ``event_metadata`` to span-safe string attributes.

    Keeps only primitive values (str/int/float/bool) under non-sensitive keys —
    never ``repr()``-ing objects, dicts, or lists, never stamping secrets/headers,
    and bounding the count and per-value length. This is the single chokepoint:
    both the GenAI and legacy mappers read the cleaned result.
    """
    if not event_metadata:
        return {}
    clean: dict[str, str] = {}
    for key, value in event_metadata.items():
        if len(clean) >= _MAX_METADATA_ITEMS:
            break
        if not isinstance(key, str) or key in _DROP_METADATA_KEYS:
            continue
        lowered = key.lower()
        if any(token in lowered for token in _SENSITIVE_METADATA_SUBSTRINGS):
            continue
        # ``bool`` is a subclass of ``int``, so it's covered. Non-primitive values
        # (objects, dicts, lists) are dropped rather than stringified.
        if isinstance(value, (str, int, float)):
            clean[key] = str(value)[:_MAX_METADATA_VALUE_LEN]
    return clean

