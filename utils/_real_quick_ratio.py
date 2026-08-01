
def _real_quick_ratio(a: str, b: str) -> float:
    # this is an upper bound on difflib.SequenceMatcher.ratio
    # similar to difflib.SequenceMatcher.real_quick_ratio, but faster since we don't instantiate
    al = len(a)
    bl = len(b)
    return 2.0 * min(al, bl) / (al + bl)

