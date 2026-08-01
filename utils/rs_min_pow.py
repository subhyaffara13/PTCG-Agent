
def rs_min_pow(expr, series_rs, a):
    """Find the minimum power of `a` in the series expansion of expr"""
    series = 0
    n = 2
    while series == 0:
        series = _rs_series(expr, series_rs, a, n)
        n *= 2
    R = series.ring
    a = R(a)
    i = R.gens.index(a)
    return min(series, key=lambda t: t[i])[i]

