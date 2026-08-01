
def _dup_zz_gcd_interpolate(h, x, K):
    """Interpolate polynomial GCD from integer GCD. """
    f = []

    while h:
        g = h % x

        if g > x // 2:
            g -= x

        f.insert(0, g)
        h = (h - g) // x

    return f

