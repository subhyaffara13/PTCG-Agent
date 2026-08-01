
def dmp_inner_gcd(f, g, u, K):
    """
    Computes polynomial GCD and cofactors of `f` and `g` in `K[X]`.

    Returns ``(h, cff, cfg)`` such that ``a = gcd(f, g)``,
    ``cff = quo(f, h)``, and ``cfg = quo(g, h)``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y, = ring("x,y", ZZ)

    >>> f = x**2 + 2*x*y + y**2
    >>> g = x**2 + x*y

    >>> R.dmp_inner_gcd(f, g)
    (x + y, x + y, x)

    """
    if not u:
        return dup_inner_gcd(f, g, K)

    J, (f, g) = dmp_multi_deflate((f, g), u, K)
    h, cff, cfg = _dmp_inner_gcd(f, g, u, K)

    return (dmp_inflate(h, J, u, K),
            dmp_inflate(cff, J, u, K),
            dmp_inflate(cfg, J, u, K))

