
def getSearchRange(n: int, itemSize: int = 16) -> tuple[int, int, int]:
    """Calculate searchRange, entrySelector, rangeShift."""
    # itemSize defaults to 16, for backward compatibility
    # with upstream fonttools.
    exponent = maxPowerOfTwo(n)
    searchRange = (2**exponent) * itemSize
    entrySelector = exponent
    rangeShift = max(0, n * itemSize - searchRange)
    return searchRange, entrySelector, rangeShift

