
def check_prev(ch: str) -> bool:
    """Return ``True`` if *ch* is a valid preceding character for an autolink."""
    return ch in _VALID_PREV_CHARS

