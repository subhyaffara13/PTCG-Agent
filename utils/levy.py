
def Levy(name, mu, c):
    r"""
    Create a continuous random variable with a Levy distribution.

    The density of the Levy distribution is given by

    .. math::
        f(x) := \sqrt(\frac{c}{2 \pi}) \frac{\exp -\frac{c}{2 (x - \mu)}}{(x - \mu)^{3/2}}

    Parameters
    ==========

    mu : Real number
        The location parameter.
    c : Real number, `c > 0`
        A scale parameter.

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Levy, density, cdf
    >>> from sympy import Symbol

    >>> mu = Symbol("mu", real=True)
    >>> c = Symbol("c", positive=True)
    >>> z = Symbol("z")

    >>> X = Levy("x", mu, c)

    >>> density(X)(z)
    sqrt(2)*sqrt(c)*exp(-c/(-2*mu + 2*z))/(2*sqrt(pi)*(-mu + z)**(3/2))

    >>> cdf(X)(z)
    erfc(sqrt(c)*sqrt(1/(-2*mu + 2*z)))

    References
    ==========
    .. [1] https://en.wikipedia.org/wiki/L%C3%A9vy_distribution
    .. [2] https://mathworld.wolfram.com/LevyDistribution.html
    """

    return rv(name, LevyDistribution, (mu, c))

