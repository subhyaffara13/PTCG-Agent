
def _safe_zero_index(x: tuple[_R, ...]) -> _R:
    if len(x) != 1:
        raise AssertionError(f"expected tuple of length 1, got length {len(x)}")
    return x[0]

