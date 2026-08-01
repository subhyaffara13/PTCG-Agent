
def subresultants(f, g, *gens, **args):
    """
    Compute subresultant PRS of ``f`` and ``g``.

    Examples
    ========

    >>> from sympy import subresultants
    >>> from sympy.abc import x

    >>> subresultants(x**2 + 1, x**2 - 1)
    [x**2 + 1, x**2 - 1, -2]

    """
    options.allowed_flags(args, ['polys'])

    try:
        (F, G), opt = parallel_poly_from_expr((f, g), *gens, **args)
    except PolificationFailed as exc:
        raise ComputationFailed('subresultants', 2, exc)

    result = F.subresultants(G)

    if not opt.polys:
        return [r.as_expr() for r in result]
    else:
        return result

