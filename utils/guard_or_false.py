
def guard_or_false(a: BoolLikeType) -> bool:
    """
    Try to guard a, if data dependent error encountered just return false.
    """
    return _guard_or(a, False)

