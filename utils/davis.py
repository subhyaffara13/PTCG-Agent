
def Davis(name, b, n, mu):
    r""" Create a continuous random variable with Davis distribution.

    Explanation
    ===========

    The density of Davis distribution is given by

    .. math::
        f(x; \mu; b, n) := \frac{b^{n}(x - \mu)^{1-n}}{ \left( e^{\frac{b}{x-\mu}} - 1 \right) \Gamma(n)\zeta(n)}

    with :math:`x \in [0,\infty]`.

    Davis distribution is a generalization of the Planck's law of radiation from statistical physics. It is used for modeling income distribution.

    Parameters
    ==========
    b : Real number
        `p > 0`, a scale.
    n : Real number
        `n > 1`, a shape.
    mu : Real number
        `mu > 0`, a location.

    Returns
    =======

    RandomSymbol

    Examples
    ========
    >>> from sympy.stats import Davis, density
    >>> from sympy import Symbol
    >>> b = Symbol("b", positive=True)
    >>> n = Symbol("n", positive=True)
    >>> mu = Symbol("mu", positive=True)
    >>> z = Symbol("z")
    >>> X = Davis("x", b, n, mu)
    >>> density(X)(z)
    b**n*(-mu + z)**(-n - 1)/((exp(b/(-mu + z)) - 1)*gamma(n)*zeta(n))

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Davis_distribution
    .. [2] https://reference.wolfram.com/language/ref/DavisDistribution.html

    """
    return rv(name, DavisDistribution, (b, n, mu))

