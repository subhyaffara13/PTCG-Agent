
def range_check(i: int, n: int) -> T | F:
    """
    Checks if an index i is within range of a size n list
    Args:
        i: index
        n: list size

    Returns: Boolean
    """
    if i >= 0:
        return T() if i < n else F()
    else:
        return T() if i >= n else F()

