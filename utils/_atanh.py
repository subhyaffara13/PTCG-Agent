
def _atanh(p, x, prec):
    """
    Expansion using formula

    Faster for very small and univariate series
    """
    R = p.ring
    one = R(1)
    c = [one]
    p2 = rs_square(p, x, prec)
    for k in range(1, prec):
        c.append(one/(2*k + 1))
    s = rs_series_from_list(p2, c, x, prec)
    s = rs_mul(s, p, x, prec)
    return s

