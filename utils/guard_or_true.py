
def guard_or_true(a: BoolLikeType) -> bool:
    """
    Try to guard a, if data dependent error encountered just return true.
    """
    return _guard_or(a, True)

