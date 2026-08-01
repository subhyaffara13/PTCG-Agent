
def NormalGamma(sym, mu, lamda, alpha, beta):
    """
    Creates a bivariate joint random variable with multivariate Normal gamma
    distribution.

    Parameters
    ==========

    sym : A symbol/str
        For identifying the random variable.
    mu : A real number
        The mean of the normal distribution
    lamda : A positive integer
        Parameter of joint distribution
    alpha : A positive integer
        Parameter of joint distribution
    beta : A positive integer
        Parameter of joint distribution

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import density, NormalGamma
    >>> from sympy import symbols

    >>> X = NormalGamma('x', 0, 1, 2, 3)
    >>> y, z = symbols('y z')

    >>> density(X)(y, z)
    9*sqrt(2)*z**(3/2)*exp(-3*z)*exp(-y**2*z/2)/(2*sqrt(pi))

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Normal-gamma_distribution

    """
    return multivariate_rv(NormalGammaDistribution, sym, mu, lamda, alpha, beta)

