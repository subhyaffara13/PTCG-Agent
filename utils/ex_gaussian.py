
def ExGaussian(name, mean, std, rate):
    r"""
    Create a continuous random variable with an Exponentially modified
    Gaussian (EMG) distribution.

    Explanation
    ===========

    The density of the exponentially modified Gaussian distribution is given by

    .. math::
        f(x) := \frac{\lambda}{2}e^{\frac{\lambda}{2}(2\mu+\lambda\sigma^2-2x)}
            \text{erfc}(\frac{\mu + \lambda\sigma^2 - x}{\sqrt{2}\sigma})

    with $x > 0$. Note that the expected value is `1/\lambda`.

    Parameters
    ==========

    name : A string giving a name for this distribution
    mean : A Real number, the mean of Gaussian component
    std : A positive Real number,
        :math: `\sigma^2 > 0` the variance of Gaussian component
    rate : A positive Real number,
        :math: `\lambda > 0` the rate of Exponential component

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import ExGaussian, density, cdf, E
    >>> from sympy.stats import variance, skewness
    >>> from sympy import Symbol, pprint, simplify

    >>> mean = Symbol("mu")
    >>> std = Symbol("sigma", positive=True)
    >>> rate = Symbol("lamda", positive=True)
    >>> z = Symbol("z")
    >>> X = ExGaussian("x", mean, std, rate)

    >>> pprint(density(X)(z), use_unicode=False)
                 /           2             \
           lamda*\lamda*sigma  + 2*mu - 2*z/
           ---------------------------------     /  ___ /           2         \\
                           2                     |\/ 2 *\lamda*sigma  + mu - z/|
    lamda*e                                 *erfc|-----------------------------|
                                                 \           2*sigma           /
    ----------------------------------------------------------------------------
                                         2

    >>> cdf(X)(z)
    -(erf(sqrt(2)*(-lamda**2*sigma**2 + lamda*(-mu + z))/(2*lamda*sigma))/2 + 1/2)*exp(lamda**2*sigma**2/2 - lamda*(-mu + z)) + erf(sqrt(2)*(-mu + z)/(2*sigma))/2 + 1/2

    >>> E(X)
    (lamda*mu + 1)/lamda

    >>> simplify(variance(X))
    sigma**2 + lamda**(-2)

    >>> simplify(skewness(X))
    2/(lamda**2*sigma**2 + 1)**(3/2)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Exponentially_modified_Gaussian_distribution
    """
    return rv(name, ExGaussianDistribution, (mean, std, rate))

