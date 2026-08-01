
def quo(f, g, *gens, **args):
    """
    Compute polynomial quotient of ``f`` and ``g``.

    Examples
    ========

    >>> from sympy import quo
    >>> from sympy.abc import x

    >>> quo(x**2 + 1, 2*x - 4)
    x/2 + 1
    >>> quo(x**2 - 1, x - 1)
    x + 1

    """
    options.allowed_flags(args, ['auto', 'polys'])

    try:
        (F, G), opt = parallel_poly_from_expr((f, g), *gens, **args)
    except PolificationFailed as exc:
        raise ComputationFailed('quo', 2, exc)

    q = F.quo(G, auto=opt.auto)

    if not opt.polys:
        return q.as_expr()
    else:
        return q

