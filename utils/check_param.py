
def check_param(x, y, a, params):
    """
    If there is a number modulo ``a`` such that ``x`` and ``y`` are both
    integers, then return a parametric representation for ``x`` and ``y``
    else return (None, None).

    Here ``x`` and ``y`` are functions of ``t``.
    """
    from sympy.simplify.simplify import clear_coefficients

    if x.is_number and not x.is_Integer:
        return DiophantineSolutionSet([x, y], parameters=params)

    if y.is_number and not y.is_Integer:
        return DiophantineSolutionSet([x, y], parameters=params)

    m, n = symbols("m, n", integer=True)
    c, p = (m*x + n*y).as_content_primitive()
    if a % c.q:
        return DiophantineSolutionSet([x, y], parameters=params)

    # clear_coefficients(mx + b, R)[1] -> (R - b)/m
    eq = clear_coefficients(x, m)[1] - clear_coefficients(y, n)[1]
    junk, eq = eq.as_content_primitive()

    return _diop_solve(eq, params=params)

