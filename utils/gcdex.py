
def gcdex(f, g, *gens, **args):
    """
    Extended Euclidean algorithm of ``f`` and ``g``.

    Returns ``(s, t, h)`` such that ``h = gcd(f, g)`` and ``s*f + t*g = h``.

    Examples
    ========

    >>> from sympy import gcdex
    >>> from sympy.abc import x

    >>> gcdex(x**4 - 2*x**3 - 6*x**2 + 12*x + 15, x**3 + x**2 - 4*x - 4)
    (3/5 - x/5, x**2/5 - 6*x/5 + 2, x + 1)

    """
    options.allowed_flags(args, ['auto', 'polys'])

    try:
        (F, G), opt = parallel_poly_from_expr((f, g), *gens, **args)
    except PolificationFailed as exc:
        domain, (a, b) = construct_domain(exc.exprs)

        try:
            s, t, h = domain.gcdex(a, b)
        except NotImplementedError:
            raise ComputationFailed('gcdex', 2, exc)
        else:
            return domain.to_sympy(s), domain.to_sympy(t), domain.to_sympy(h)

    s, t, h = F.gcdex(G, auto=opt.auto)

    if not opt.polys:
        return s.as_expr(), t.as_expr(), h.as_expr()
    else:
        return s, t, h

