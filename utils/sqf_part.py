
def sqf_part(f, *gens, **args):
    """
    Compute square-free part of ``f``.

    Examples
    ========

    >>> from sympy import sqf_part
    >>> from sympy.abc import x

    >>> sqf_part(x**3 - 3*x - 2)
    x**2 - x - 2

    """
    options.allowed_flags(args, ['polys'])

    try:
        F, opt = poly_from_expr(f, *gens, **args)
    except PolificationFailed as exc:
        raise ComputationFailed('sqf_part', 1, exc)

    result = F.sqf_part()

    if not opt.polys:
        return result.as_expr()
    else:
        return result

