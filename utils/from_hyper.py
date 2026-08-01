
def from_hyper(func, x0=0, evalf=False):
    r"""
    Converts a hypergeometric function to holonomic.
    ``func`` is the Hypergeometric Function and ``x0`` is the point at
    which initial conditions are required.

    Examples
    ========

    >>> from sympy.holonomic.holonomic import from_hyper
    >>> from sympy import symbols, hyper, S
    >>> x = symbols('x')
    >>> from_hyper(hyper([], [S(3)/2], x**2/4))
    HolonomicFunction((-x) + (2)*Dx + (x)*Dx**2, x, 1, [sinh(1), -sinh(1) + cosh(1)])
    """

    a = func.ap
    b = func.bq
    z = func.args[2]
    x = z.atoms(Symbol).pop()
    R, Dx = DifferentialOperators(QQ.old_poly_ring(x), 'Dx')

    # generalized hypergeometric differential equation
    xDx = x*Dx
    r1 = 1
    for ai in a:  # XXX gives sympify error if Mul is used with list of all factors
        r1 *= xDx + ai
    xDx_1 = xDx - 1
    # r2 = Mul(*([Dx] + [xDx_1 + bi for bi in b]))  # XXX gives sympify error
    r2 = Dx
    for bi in b:
        r2 *= xDx_1 + bi
    sol = r1 - r2

    simp = hyperexpand(func)

    if simp in (Infinity, NegativeInfinity):
        return HolonomicFunction(sol, x).composition(z)

    # if the function is known symbolically
    if not isinstance(simp, hyper):
        y0 = _find_conditions(simp, x, x0, sol.order, use_limit=False)
        while not y0:
            # if values don't exist at 0, then try to find initial
            # conditions at 1. If it doesn't exist at 1 too then
            # try 2 and so on.
            x0 += 1
            y0 = _find_conditions(simp, x, x0, sol.order, use_limit=False)

        return HolonomicFunction(sol, x).composition(z, x0, y0)

    if isinstance(simp, hyper):
        x0 = 1
        # use evalf if the function can't be simplified
        y0 = _find_conditions(simp, x, x0, sol.order, evalf, use_limit=False)
        while not y0:
            x0 += 1
            y0 = _find_conditions(simp, x, x0, sol.order, evalf, use_limit=False)
        return HolonomicFunction(sol, x).composition(z, x0, y0)

    return HolonomicFunction(sol, x).composition(z)

