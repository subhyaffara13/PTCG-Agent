
def unicode_range(character: str) -> str | None:
    """
    Retrieve the Unicode range official name from a single character.
    """
    character_ord: int = ord(character)

    # Binary search: find the rightmost range whose start <= character_ord
    idx = bisect_right(_UNICODE_RANGE_STARTS, character_ord) - 1
    if idx >= 0:
        start, stop, name = _UNICODE_RANGES_SORTED[idx]
        if character_ord < stop:
            return name

    return None

