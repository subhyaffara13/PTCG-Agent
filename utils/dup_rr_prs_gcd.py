
def dup_rr_prs_gcd(f, g, K):
    """
    Computes polynomial GCD using subresultants over a ring.

    Returns ``(h, cff, cfg)`` such that ``a = gcd(f, g)``, ``cff = quo(f, h)``,
    and ``cfg = quo(g, h)``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_rr_prs_gcd(x**2 - 1, x**2 - 3*x + 2)
    (x - 1, x + 1, x - 2)

    """
    result = _dup_rr_trivial_gcd(f, g, K)

    if result is not None:
        return result

    fc, F = dup_primitive(f, K)
    gc, G = dup_primitive(g, K)

    c = K.gcd(fc, gc)

    h = dup_subresultants(F, G, K)[-1]
    _, h = dup_primitive(h, K)

    c *= K.canonical_unit(dup_LC(h, K))

    h = dup_mul_ground(h, c, K)

    cff = dup_quo(f, h, K)
    cfg = dup_quo(g, h, K)

    return h, cff, cfg

