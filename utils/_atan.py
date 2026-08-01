
def _atan(p, iv, prec):
    """
    Expansion using formula.

    Faster on very small and univariate series.
    """
    R = p.ring
    mo = R(-1)
    c = [-mo]
    p2 = rs_square(p, iv, prec)
    for k in range(1, prec):
        c.append(mo**k/(2*k + 1))
    s = rs_series_from_list(p2, c, iv, prec)
    s = rs_mul(s, p, iv, prec)
    return s

