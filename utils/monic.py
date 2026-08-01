
def monic(f, *gens, **args):
    """
    Divide all coefficients of ``f`` by ``LC(f)``.

    Examples
    ========

    >>> from sympy import monic
    >>> from sympy.abc import x

    >>> monic(3*x**2 + 4*x + 2)
    x**2 + 4*x/3 + 2/3

    """
    options.allowed_flags(args, ['auto', 'polys'])

    try:
        F, opt = poly_from_expr(f, *gens, **args)
    except PolificationFailed as exc:
        raise ComputationFailed('monic', 1, exc)

    result = F.monic(auto=opt.auto)

    if not opt.polys:
        return result.as_expr()
    else:
        return result

