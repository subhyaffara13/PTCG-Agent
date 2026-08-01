
def ode_1st_power_series(eq, func, order, match):
    r"""
    The power series solution is a method which gives the Taylor series expansion
    to the solution of a differential equation.

    For a first order differential equation `\frac{dy}{dx} = h(x, y)`, a power
    series solution exists at a point `x = x_{0}` if `h(x, y)` is analytic at `x_{0}`.
    The solution is given by

    .. math:: y(x) = y(x_{0}) + \sum_{n = 1}^{\infty} \frac{F_{n}(x_{0},b)(x - x_{0})^n}{n!},

    where `y(x_{0}) = b` is the value of y at the initial value of `x_{0}`.
    To compute the values of the `F_{n}(x_{0},b)` the following algorithm is
    followed, until the required number of terms are generated.

    1. `F_1 = h(x_{0}, b)`
    2. `F_{n+1} = \frac{\partial F_{n}}{\partial x} + \frac{\partial F_{n}}{\partial y}F_{1}`

    Examples
    ========

    >>> from sympy import Function, pprint, exp, dsolve
    >>> from sympy.abc import x
    >>> f = Function('f')
    >>> eq = exp(x)*(f(x).diff(x)) - f(x)
    >>> pprint(dsolve(eq, hint='1st_power_series'))
                           3       4       5
                       C1*x    C1*x    C1*x     / 6\
    f(x) = C1 + C1*x - ----- + ----- + ----- + O\x /
                         6       24      60


    References
    ==========

    - Travis W. Walker, Analytic power series technique for solving first-order
      differential equations, p.p 17, 18

    """
    x = func.args[0]
    y = match['y']
    f = func.func
    h = -match[match['d']]/match[match['e']]
    point = match['f0']
    value = match['f0val']
    terms = match['terms']

    # First term
    F = h
    if not h:
        return Eq(f(x), value)

    # Initialization
    series = value
    if terms > 1:
        hc = h.subs({x: point, y: value})
        if hc.has(oo) or hc.has(nan) or hc.has(zoo):
            # Derivative does not exist, not analytic
            return Eq(f(x), oo)
        elif hc:
            series += hc*(x - point)

    for factcount in range(2, terms):
        Fnew = F.diff(x) + F.diff(y)*h
        Fnewc = Fnew.subs({x: point, y: value})
        # Same logic as above
        if Fnewc.has(oo) or Fnewc.has(nan) or Fnewc.has(-oo) or Fnewc.has(zoo):
            return Eq(f(x), oo)
        series += Fnewc*((x - point)**factcount)/factorial(factcount)
        F = Fnew
    series += Order(x**terms)
    return Eq(f(x), series)

