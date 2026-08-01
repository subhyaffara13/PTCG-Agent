
def _split_type(location: str, *, raw: str) -> tuple[constants.HfUriType, str]:
    """Detect the (optional) type prefix and return '(type, remaining_location)'.

    A missing type prefix defaults to 'model'. Singular forms ('model/', 'dataset/', etc.) are explicitly rejected with a helpful error.
    """
    slash_idx = location.find("/")
    if slash_idx == -1:
        # Single segment, no prefix. Reject if it looks like a bare type name.
        if location in constants.HF_URI_TYPE_PREFIXES:
            raise HfUriError(
                uri=raw,
                msg=f"Missing identifier after '{location}'. Expected '{constants.HF_PROTOCOL}{location}/<ID>'.",
            )
        if (singular_plural := _TYPE_TO_PREFIX.get(location)) is not None:
            raise HfUriError(
                uri=raw,
                msg=f"Type prefix must be plural. Did you mean '{constants.HF_PROTOCOL}{singular_plural}/...'?",
            )
        return "model", location

    first = location[:slash_idx]
    rest = location[slash_idx + 1 :]
    if first in constants.HF_URI_TYPE_PREFIXES:
        return constants.HF_URI_TYPE_PREFIXES[first], rest
    if (singular_plural := _TYPE_TO_PREFIX.get(first)) is not None:
        raise HfUriError(
            uri=raw, msg=f"Type prefix must be plural, got '{first}/'. Did you mean '{singular_plural}/'?"
        )
    return "model", location

