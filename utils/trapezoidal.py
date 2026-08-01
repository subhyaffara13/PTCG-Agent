
def Trapezoidal(name, a, b, c, d):
    r"""
    Create a continuous random variable with a trapezoidal distribution.

    Explanation
    ===========

    The density of the trapezoidal distribution is given by

    .. math::
        f(x) := \begin{cases}
                  0 & \mathrm{for\ } x < a, \\
                  \frac{2(x-a)}{(b-a)(d+c-a-b)} & \mathrm{for\ } a \le x < b, \\
                  \frac{2}{d+c-a-b} & \mathrm{for\ } b \le x < c, \\
                  \frac{2(d-x)}{(d-c)(d+c-a-b)} & \mathrm{for\ } c \le x < d, \\
                  0 & \mathrm{for\ } d < x.
                \end{cases}

    Parameters
    ==========

    a : Real number, :math:`a < d`
    b : Real number, :math:`a \le b < c`
    c : Real number, :math:`b < c \le d`
    d : Real number

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Trapezoidal, density
    >>> from sympy import Symbol, pprint

    >>> a = Symbol("a")
    >>> b = Symbol("b")
    >>> c = Symbol("c")
    >>> d = Symbol("d")
    >>> z = Symbol("z")

    >>> X = Trapezoidal("x", a,b,c,d)

    >>> pprint(density(X)(z), use_unicode=False)
    /        -2*a + 2*z
    |-------------------------  for And(a <= z, b > z)
    |(-a + b)*(-a - b + c + d)
    |
    |           2
    |     --------------        for And(b <= z, c > z)
    <     -a - b + c + d
    |
    |        2*d - 2*z
    |-------------------------  for And(d >= z, c <= z)
    |(-c + d)*(-a - b + c + d)
    |
    \            0                     otherwise

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Trapezoidal_distribution

    """
    return rv(name, TrapezoidalDistribution, (a, b, c, d))

