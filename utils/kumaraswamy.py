
def Kumaraswamy(name, a, b):
    r"""
    Create a Continuous Random Variable with a Kumaraswamy distribution.

    Explanation
    ===========

    The density of the Kumaraswamy distribution is given by

    .. math::
        f(x) := a b x^{a-1} (1-x^a)^{b-1}

    with :math:`x \in [0,1]`.

    Parameters
    ==========

    a : Real number, `a > 0`, a shape
    b : Real number, `b > 0`, a shape

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Kumaraswamy, density, cdf
    >>> from sympy import Symbol, pprint

    >>> a = Symbol("a", positive=True)
    >>> b = Symbol("b", positive=True)
    >>> z = Symbol("z")

    >>> X = Kumaraswamy("x", a, b)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
                       b - 1
         a - 1 /     a\
    a*b*z     *\1 - z /

    >>> cdf(X)(z)
    Piecewise((0, z < 0), (1 - (1 - z**a)**b, z <= 1), (1, True))

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Kumaraswamy_distribution

    """

    return rv(name, KumaraswamyDistribution, (a, b))

