
def dup_inner_gcd(f, g, K):
    """
    Computes polynomial GCD and cofactors of `f` and `g` in `K[x]`.

    Returns ``(h, cff, cfg)`` such that ``a = gcd(f, g)``,
    ``cff = quo(f, h)``, and ``cfg = quo(g, h)``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_inner_gcd(x**2 - 1, x**2 - 3*x + 2)
    (x - 1, x + 1, x - 2)

    """
    # XXX: This used to check for K.is_Exact but leads to awkward results when
    # the domain is something like RR[z] e.g.:
    #
    # >>> g, p, q = Poly(1, x).cancel(Poly(51.05*x*y - 1.0, x))
    # >>> g
    # 1.0
    # >>> p
    # Poly(17592186044421.0, x, domain='RR[y]')
    # >>> q
    # Poly(898081097567692.0*y*x - 17592186044421.0, x, domain='RR[y]'))
    #
    # Maybe it would be better to flatten into multivariate polynomials first.
    if K.is_RR or K.is_CC:
        try:
            exact = K.get_exact()
        except DomainError:
            return [K.one], f, g

        f = dup_convert(f, K, exact)
        g = dup_convert(g, K, exact)

        h, cff, cfg = dup_inner_gcd(f, g, exact)

        h = dup_convert(h, exact, K)
        cff = dup_convert(cff, exact, K)
        cfg = dup_convert(cfg, exact, K)

        return h, cff, cfg
    elif K.is_Field:
        if K.is_QQ and query('USE_HEU_GCD'):
            try:
                return dup_qq_heu_gcd(f, g, K)
            except HeuristicGCDFailed:
                pass

        return dup_ff_prs_gcd(f, g, K)
    else:
        if K.is_ZZ and query('USE_HEU_GCD'):
            try:
                return dup_zz_heu_gcd(f, g, K)
            except HeuristicGCDFailed:
                pass

        return dup_rr_prs_gcd(f, g, K)

