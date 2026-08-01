
def components(f, x):
    """
    Returns a set of all functional components of the given expression
    which includes symbols, function applications and compositions and
    non-integer powers. Fractional powers are collected with
    minimal, positive exponents.

    Examples
    ========

    >>> from sympy import cos, sin
    >>> from sympy.abc import x
    >>> from sympy.integrals.heurisch import components

    >>> components(sin(x)*cos(x)**2, x)
    {x, sin(x), cos(x)}

    See Also
    ========

    heurisch
    """
    result = set()

    if f.has_free(x):
        if f.is_symbol and f.is_commutative:
            result.add(f)
        elif f.is_Function or f.is_Derivative:
            for g in f.args:
                result |= components(g, x)

            result.add(f)
        elif f.is_Pow:
            result |= components(f.base, x)

            if not f.exp.is_Integer:
                if f.exp.is_Rational:
                    result.add(f.base**Rational(1, f.exp.q))
                else:
                    result |= components(f.exp, x) | {f}
        else:
            for g in f.args:
                result |= components(g, x)

    return result

