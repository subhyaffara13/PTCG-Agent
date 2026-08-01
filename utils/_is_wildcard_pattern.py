
def _is_wildcard_pattern(allowed_model_pattern: str) -> bool:
    """
    Returns True if the pattern is a wildcard pattern.

    Checks if `*` is in the pattern.
    """
    return "*" in allowed_model_pattern

