
def dup_ff_prs_gcd(f, g, K):
    """
    Computes polynomial GCD using subresultants over a field.

    Returns ``(h, cff, cfg)`` such that ``a = gcd(f, g)``, ``cff = quo(f, h)``,
    and ``cfg = quo(g, h)``.

    Examples
    ========

    >>> from sympy.polys import ring, QQ
    >>> R, x = ring("x", QQ)

    >>> R.dup_ff_prs_gcd(x**2 - 1, x**2 - 3*x + 2)
    (x - 1, x + 1, x - 2)

    """
    result = _dup_ff_trivial_gcd(f, g, K)

    if result is not None:
        return result

    h = dup_subresultants(f, g, K)[-1]
    h = dup_monic(h, K)

    cff = dup_quo(f, h, K)
    cfg = dup_quo(g, h, K)

    return h, cff, cfg

