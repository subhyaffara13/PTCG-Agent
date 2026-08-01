
def get_finest_unit(left: str, right: str) -> str:
    """
    Find the higher of two datetime64 units.
    """
    if _UNITS.index(left) >= _UNITS.index(right):
        return left
    return right

