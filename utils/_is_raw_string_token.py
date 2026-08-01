
def _is_raw_string_token(token: str) -> bool:
    """Return whether a string token is a raw string (has an ``r``/``R`` prefix).

    Only the prefix markers that precede the opening quote are inspected, e.g.
    ``r"foo"`` and ``Rb"foo"`` are raw while ``"foo"`` and ``f"foo"`` are not.
    """
    for char in token:
        if char in "'\"":
            break
        if char in "rR":
            return True
    return False

