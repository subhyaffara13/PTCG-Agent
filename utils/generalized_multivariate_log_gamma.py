
def GeneralizedMultivariateLogGamma(syms, delta, v, lamda, mu):
    """
    Creates a joint random variable with generalized multivariate log gamma
    distribution.

    The joint pdf can be found at [1].

    Parameters
    ==========

    syms : list/tuple/set of symbols for identifying each component
    delta : A constant in range $[0, 1]$
    v : Positive real number
    lamda : List of positive real numbers
    mu : List of positive real numbers

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import density
    >>> from sympy.stats.joint_rv_types import GeneralizedMultivariateLogGamma
    >>> from sympy import symbols, S
    >>> v = 1
    >>> l, mu = [1, 1, 1], [1, 1, 1]
    >>> d = S.Half
    >>> y = symbols('y_1:4', positive=True)
    >>> Gd = GeneralizedMultivariateLogGamma('G', d, v, l, mu)
    >>> density(Gd)(y[0], y[1], y[2])
    Sum(exp((n + 1)*(y_1 + y_2 + y_3) - exp(y_1) - exp(y_2) -
    exp(y_3))/(2**n*gamma(n + 1)**3), (n, 0, oo))/2

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Generalized_multivariate_log-gamma_distribution
    .. [2] https://www.researchgate.net/publication/234137346_On_a_multivariate_log-gamma_distribution_and_the_use_of_the_distribution_in_the_Bayesian_analysis

    Note
    ====

    If the GeneralizedMultivariateLogGamma is too long to type use,

    >>> from sympy.stats.joint_rv_types import GeneralizedMultivariateLogGamma as GMVLG
    >>> Gd = GMVLG('G', d, v, l, mu)

    If you want to pass the matrix omega instead of the constant delta, then use
    ``GeneralizedMultivariateLogGammaOmega``.

    """
    return multivariate_rv(GeneralizedMultivariateLogGammaDistribution,
                            syms, delta, v, lamda, mu)

