
def _lexsort_depth(codes: list[np.ndarray], nlevels: int) -> int:
    """Count depth (up to a maximum of `nlevels`) with which codes are lexsorted."""
    int64_codes = [ensure_int64(level_codes) for level_codes in codes]
    for k in range(nlevels, 0, -1):
        if libalgos.is_lexsorted(int64_codes[:k]):
            return k
    return 0

