
def refine_root(f, s, t, eps=None, steps=None, fast=False, check_sqf=False):
    """
    Refine an isolating interval of a root to the given precision.

    Examples
    ========

    >>> from sympy import refine_root
    >>> from sympy.abc import x

    >>> refine_root(x**2 - 3, 1, 2, eps=1e-2)
    (19/11, 26/15)

    """
    try:
        F = Poly(f)
        if not isinstance(f, Poly) and not F.gen.is_Symbol:
            # root of sin(x) + 1 is -1 but when someone
            # passes an Expr instead of Poly they may not expect
            # that the generator will be sin(x), not x
            raise PolynomialError("generator must be a Symbol")
    except GeneratorsNeeded:
        raise PolynomialError(
            "Cannot refine a root of %s, not a polynomial" % f)

    return F.refine_root(s, t, eps=eps, steps=steps, fast=fast, check_sqf=check_sqf)

