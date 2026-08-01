
def diff_string(old: float, new: float) -> str:
    """Given an old and new value, return a string representing the difference."""
    diff = abs(old - new)
    diff_str = f"{CMPS[cmp(old, new)]}{(diff and f'{diff:.2f}') or ''}"
    return diff_str

