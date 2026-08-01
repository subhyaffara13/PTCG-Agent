
def GammaInverse(name, a, b):
    r"""
    Create a continuous random variable with an inverse Gamma distribution.

    Explanation
    ===========

    The density of the inverse Gamma distribution is given by

    .. math::
        f(x) := \frac{\beta^\alpha}{\Gamma(\alpha)} x^{-\alpha - 1}
                \exp\left(\frac{-\beta}{x}\right)

    with :math:`x > 0`.

    Parameters
    ==========

    a : Real number, `a > 0`, a shape
    b : Real number, `b > 0`, a scale

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import GammaInverse, density, cdf
    >>> from sympy import Symbol, pprint

    >>> a = Symbol("a", positive=True)
    >>> b = Symbol("b", positive=True)
    >>> z = Symbol("z")

    >>> X = GammaInverse("x", a, b)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
                -b
                ---
     a  -a - 1   z
    b *z      *e
    ---------------
       Gamma(a)

    >>> cdf(X)(z)
    Piecewise((uppergamma(a, b/z)/gamma(a), z > 0), (0, True))


    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Inverse-gamma_distribution

    """

    return rv(name, GammaInverseDistribution, (a, b))

