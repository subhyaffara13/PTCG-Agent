
def Moyal(name, mu, sigma):
    r"""
    Create a continuous random variable with a Moyal distribution.

    Explanation
    ===========

    The density of the Moyal distribution is given by

    .. math::
        f(x) := \frac{\exp-\frac{1}{2}\exp-\frac{x-\mu}{\sigma}-\frac{x-\mu}{2\sigma}}{\sqrt{2\pi}\sigma}

    with :math:`x \in \mathbb{R}`.

    Parameters
    ==========

    mu : Real number
        Location parameter
    sigma : Real positive number
        Scale parameter

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Moyal, density, cdf
    >>> from sympy import Symbol, simplify
    >>> mu = Symbol("mu", real=True)
    >>> sigma = Symbol("sigma", positive=True, real=True)
    >>> z = Symbol("z")
    >>> X = Moyal("x", mu, sigma)
    >>> density(X)(z)
    sqrt(2)*exp(-exp((mu - z)/sigma)/2 - (-mu + z)/(2*sigma))/(2*sqrt(pi)*sigma)
    >>> simplify(cdf(X)(z))
    1 - erf(sqrt(2)*exp((mu - z)/(2*sigma))/2)

    References
    ==========

    .. [1] https://reference.wolfram.com/language/ref/MoyalDistribution.html
    .. [2] https://www.stat.rice.edu/~dobelman/textfiles/DistributionsHandbook.pdf

    """

    return rv(name, MoyalDistribution, (mu, sigma))

