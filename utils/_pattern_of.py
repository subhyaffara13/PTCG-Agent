
def _pattern_of(key: str) -> str:
    """Replace every dot-delimited integer with '*' to get the structure."""
    return _DIGIT_RX.sub("*", key)

