
def splitUp(pred):
    """Parse a single version comparison.

    Return (comparison string, StrictVersion)
    """
    res = re_splitComparison.match(pred)
    if not res:
        raise ValueError(f"bad package restriction syntax: {pred!r}")
    comp, verStr = res.groups()
    with version.suppress_known_deprecation():
        other = version.StrictVersion(verStr)
    return (comp, other)

