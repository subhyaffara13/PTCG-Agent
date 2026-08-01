
def _range_is_empty(lower: _LowerBound, upper: _UpperBound) -> bool:
    """True when the range defined by *lower* and *upper* contains no versions."""
    if lower.version is None or upper.version is None:
        return False
    if lower.version == upper.version:
        return not (lower.inclusive and upper.inclusive)
    return lower.version > upper.version


def _range_is_empty(lower: _LowerBound, upper: _UpperBound) -> bool:
    """True when the range defined by *lower* and *upper* contains no versions."""
    if lower.version is None or upper.version is None:
        return False
    if lower.version == upper.version:
        return not (lower.inclusive and upper.inclusive)
    return lower.version > upper.version

