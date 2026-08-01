
def dup_rr_lcm(f, g, K):
    """
    Computes polynomial LCM over a ring in `K[x]`.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_rr_lcm(x**2 - 1, x**2 - 3*x + 2)
    x**3 - 2*x**2 - x + 2

    """
    if not f or not g:
        return dmp_zero(0)

    fc, f = dup_primitive(f, K)
    gc, g = dup_primitive(g, K)

    c = K.lcm(fc, gc)

    h = dup_quo(dup_mul(f, g, K),
                dup_gcd(f, g, K), K)

    u = K.canonical_unit(dup_LC(h, K))

    return dup_mul_ground(h, c*u, K)

