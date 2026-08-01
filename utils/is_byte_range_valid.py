
def is_byte_range_valid(
    start: int | None, stop: int | None, length: int | None
) -> bool:
    """Checks if a given byte content range is valid for the given length.

    .. versionadded:: 0.7
    """
    if (start is None) != (stop is None):
        return False
    elif start is None:
        return length is None or length >= 0
    elif length is None:
        return 0 <= start < stop  # type: ignore
    elif start >= stop:  # type: ignore
        return False
    return 0 <= start < length

