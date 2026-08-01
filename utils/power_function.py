
def PowerFunction(name, alpha, a, b):
    r"""
    Creates a continuous random variable with a Power Function Distribution.

    Explanation
    ===========

    The density of PowerFunction distribution is given by

    .. math::
        f(x) := \frac{{\alpha}(x - a)^{\alpha - 1}}{(b - a)^{\alpha}}

    with :math:`x \in [a,b]`.

    Parameters
    ==========

    alpha : Positive number, `0 < \alpha`, the shape parameter
    a : Real number, :math:`-\infty < a`, the left boundary
    b : Real number, :math:`a < b < \infty`, the right boundary

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import PowerFunction, density, cdf, E, variance
    >>> from sympy import Symbol
    >>> alpha = Symbol("alpha", positive=True)
    >>> a = Symbol("a", real=True)
    >>> b = Symbol("b", real=True)
    >>> z = Symbol("z")

    >>> X = PowerFunction("X", 2, a, b)

    >>> density(X)(z)
    (-2*a + 2*z)/(-a + b)**2

    >>> cdf(X)(z)
    Piecewise((a**2/(a**2 - 2*a*b + b**2) - 2*a*z/(a**2 - 2*a*b + b**2) +
    z**2/(a**2 - 2*a*b + b**2), a <= z), (0, True))

    >>> alpha = 2
    >>> a = 0
    >>> b = 1
    >>> Y = PowerFunction("Y", alpha, a, b)

    >>> E(Y)
    2/3

    >>> variance(Y)
    1/18

    References
    ==========

    .. [1] https://web.archive.org/web/20200204081320/http://www.mathwave.com/help/easyfit/html/analyses/distributions/power_func.html

    """
    return rv(name, PowerFunctionDistribution, (alpha, a, b))

