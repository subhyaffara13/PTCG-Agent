
def GaussianInverse(name, mean, shape):
    r"""
    Create a continuous random variable with an Inverse Gaussian distribution.
    Inverse Gaussian distribution is also known as Wald distribution.

    Explanation
    ===========

    The density of the Inverse Gaussian distribution is given by

    .. math::
        f(x) := \sqrt{\frac{\lambda}{2\pi x^3}} e^{-\frac{\lambda(x-\mu)^2}{2x\mu^2}}

    Parameters
    ==========

    mu :
        Positive number representing the mean.
    lambda :
        Positive number representing the shape parameter.

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import GaussianInverse, density, E, std, skewness
    >>> from sympy import Symbol, pprint

    >>> mu = Symbol("mu", positive=True)
    >>> lamda = Symbol("lambda", positive=True)
    >>> z = Symbol("z", positive=True)
    >>> X = GaussianInverse("x", mu, lamda)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
                                       2
                      -lambda*(-mu + z)
                      -------------------
                                2
      ___   ________        2*mu *z
    \/ 2 *\/ lambda *e
    -------------------------------------
                    ____  3/2
                2*\/ pi *z

    >>> E(X)
    mu

    >>> std(X).expand()
    mu**(3/2)/sqrt(lambda)

    >>> skewness(X).expand()
    3*sqrt(mu)/sqrt(lambda)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Inverse_Gaussian_distribution
    .. [2] https://mathworld.wolfram.com/InverseGaussianDistribution.html

    """

    return rv(name, GaussianInverseDistribution, (mean, shape))

