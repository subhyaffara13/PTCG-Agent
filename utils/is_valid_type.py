
def is_valid_type(s: str) -> bool:
    """Try to determine whether a string might be a valid type annotation."""
    if s in ("True", "False", "retval"):
        return False
    if "," in s and "[" not in s:
        return False
    return _TYPE_RE.match(s) is not None

