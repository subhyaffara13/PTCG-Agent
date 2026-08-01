
def _is_valid_utf8(s: str) -> bool:
    if 0 <= ord(s) < _SURROGATE_MIN:
        return True
    if _SURROGATE_MAX < ord(s) <= maxunicode:
        return True
    return False

