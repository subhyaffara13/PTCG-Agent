
def bisect_left(a: list[Any], x: Any, lo: int = 0, hi: int = -1) -> int:
    """Same as https://docs.python.org/3/library/bisect.html; not in numba yet!"""
    if hi == -1:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

