
def exquo(f, g, *gens, **args):
    """
    Compute polynomial exact quotient of ``f`` and ``g``.

    Examples
    ========

    >>> from sympy import exquo
    >>> from sympy.abc import x

    >>> exquo(x**2 - 1, x - 1)
    x + 1

    >>> exquo(x**2 + 1, 2*x - 4)
    Traceback (most recent call last):
    ...
    ExactQuotientFailed: 2*x - 4 does not divide x**2 + 1

    """
    options.allowed_flags(args, ['auto', 'polys'])

    try:
        (F, G), opt = parallel_poly_from_expr((f, g), *gens, **args)
    except PolificationFailed as exc:
        raise ComputationFailed('exquo', 2, exc)

    q = F.exquo(G, auto=opt.auto)

    if not opt.polys:
        return q.as_expr()
    else:
        return q

