
def _treeHeight(branchFactor: int, maxValue: int) -> int:
    """Return the minimum tree height needed to represent maxValue."""
    height = 1
    capacity = branchFactor
    while capacity <= maxValue:
        capacity *= branchFactor
        height += 1
    return height

