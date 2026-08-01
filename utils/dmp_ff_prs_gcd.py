
def dmp_ff_prs_gcd(f, g, u, K):
    """
    Computes polynomial GCD using subresultants over a field.

    Returns ``(h, cff, cfg)`` such that ``a = gcd(f, g)``, ``cff = quo(f, h)``,
    and ``cfg = quo(g, h)``.

    Examples
    ========

    >>> from sympy.polys import ring, QQ
    >>> R, x,y, = ring("x,y", QQ)

    >>> f = QQ(1,2)*x**2 + x*y + QQ(1,2)*y**2
    >>> g = x**2 + x*y

    >>> R.dmp_ff_prs_gcd(f, g)
    (x + y, 1/2*x + 1/2*y, x)

    """
    if not u:
        return dup_ff_prs_gcd(f, g, K)

    result = _dmp_ff_trivial_gcd(f, g, u, K)

    if result is not None:
        return result

    fc, F = dmp_primitive(f, u, K)
    gc, G = dmp_primitive(g, u, K)

    h = dmp_subresultants(F, G, u, K)[-1]
    c, _, _ = dmp_ff_prs_gcd(fc, gc, u - 1, K)

    _, h = dmp_primitive(h, u, K)
    h = dmp_mul_term(h, c, 0, u, K)
    h = dmp_ground_monic(h, u, K)

    cff = dmp_quo(f, h, u, K)
    cfg = dmp_quo(g, h, u, K)

    return h, cff, cfg

