
def _visible_ljust(s: str, width: int) -> str:
    """Left-justify a string to the given visible width, ignoring OSC 8 escapes."""
    return s + " " * (width - _visible_len(s))

