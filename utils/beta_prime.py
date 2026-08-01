
def BetaPrime(name, alpha, beta):
    r"""
    Create a continuous random variable with a Beta prime distribution.

    The density of the Beta prime distribution is given by

    .. math::
        f(x) := \frac{x^{\alpha-1} (1+x)^{-\alpha -\beta}}{B(\alpha,\beta)}

    with :math:`x > 0`.

    Parameters
    ==========

    alpha : Real number, `\alpha > 0`, a shape
    beta : Real number, `\beta > 0`, a shape

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import BetaPrime, density
    >>> from sympy import Symbol, pprint

    >>> alpha = Symbol("alpha", positive=True)
    >>> beta = Symbol("beta", positive=True)
    >>> z = Symbol("z")

    >>> X = BetaPrime("x", alpha, beta)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
     alpha - 1        -alpha - beta
    z         *(z + 1)
    -------------------------------
             B(alpha, beta)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Beta_prime_distribution
    .. [2] https://mathworld.wolfram.com/BetaPrimeDistribution.html

    """

    return rv(name, BetaPrimeDistribution, (alpha, beta))

