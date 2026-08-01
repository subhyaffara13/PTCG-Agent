
def nancorr(
    a: np.ndarray,
    b: np.ndarray,
    *,
    method: CorrelationMethod = "pearson",
    min_periods: int | None = None,
) -> float:
    """
    a, b: ndarrays
    """
    if len(a) != len(b):
        raise AssertionError("Operands to nancorr must have same size")

    if min_periods is None:
        min_periods = 1

    valid = notna(a) & notna(b)
    if not valid.all():
        a = a[valid]
        b = b[valid]

    if len(a) < min_periods:
        return np.nan

    a = _ensure_numeric(a)
    b = _ensure_numeric(b)

    f = get_corr_func(method)
    return f(a, b)

