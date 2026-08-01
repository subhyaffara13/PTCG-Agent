
def Lomax(name, alpha, lamda):
    r"""
    Create a continuous random variable with a Lomax distribution.

    Explanation
    ===========

    The density of the Lomax distribution is given by

    .. math::
        f(x) := \frac{\alpha}{\lambda}\left[1+\frac{x}{\lambda}\right]^{-(\alpha+1)}

    Parameters
    ==========

    alpha : Real Number, `\alpha > 0`
        Shape parameter
    lamda : Real Number, `\lambda > 0`
        Scale parameter

    Examples
    ========

    >>> from sympy.stats import Lomax, density, cdf, E
    >>> from sympy import symbols
    >>> a, l = symbols('a, l', positive=True)
    >>> X = Lomax('X', a, l)
    >>> x = symbols('x')
    >>> density(X)(x)
    a*(1 + x/l)**(-a - 1)/l
    >>> cdf(X)(x)
    Piecewise((1 - 1/(1 + x/l)**a, x >= 0), (0, True))
    >>> a = 2
    >>> X = Lomax('X', a, l)
    >>> E(X)
    l

    Returns
    =======

    RandomSymbol

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Lomax_distribution

    """
    return rv(name, LomaxDistribution, (alpha, lamda))

