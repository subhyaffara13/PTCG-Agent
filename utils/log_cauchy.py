
def LogCauchy(name, mu, sigma):
    r"""
    Create a continuous random variable with a Log-Cauchy distribution.
    The density of the Log-Cauchy distribution is given by

    .. math::
        f(x) := \frac{1}{\pi x} \frac{\sigma}{(log(x)-\mu^2) + \sigma^2}

    Parameters
    ==========

    mu : Real number, the location

    sigma : Real number, `\sigma > 0`, a scale

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import LogCauchy, density, cdf
    >>> from sympy import Symbol, S

    >>> mu = 2
    >>> sigma = S.One / 5
    >>> z = Symbol("z")

    >>> X = LogCauchy("x", mu, sigma)

    >>> density(X)(z)
    1/(5*pi*z*((log(z) - 2)**2 + 1/25))

    >>> cdf(X)(z)
    atan(5*log(z) - 10)/pi + 1/2

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Log-Cauchy_distribution
    """

    return rv(name, LogCauchyDistribution, (mu, sigma))

