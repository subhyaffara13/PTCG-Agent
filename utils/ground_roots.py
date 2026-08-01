
def ground_roots(f, *gens, **args):
    """
    Compute roots of ``f`` by factorization in the ground domain.

    Examples
    ========

    >>> from sympy import ground_roots
    >>> from sympy.abc import x

    >>> ground_roots(x**6 - 4*x**4 + 4*x**3 - x**2)
    {0: 2, 1: 2}

    """
    options.allowed_flags(args, [])

    try:
        F, opt = poly_from_expr(f, *gens, **args)
        if not isinstance(f, Poly) and not F.gen.is_Symbol:
            # root of sin(x) + 1 is -1 but when someone
            # passes an Expr instead of Poly they may not expect
            # that the generator will be sin(x), not x
            raise PolynomialError("generator must be a Symbol")
    except PolificationFailed as exc:
        raise ComputationFailed('ground_roots', 1, exc)

    return F.ground_roots()

