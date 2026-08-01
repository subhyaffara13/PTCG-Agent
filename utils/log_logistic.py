
def LogLogistic(name, alpha, beta):
    r"""
    Create a continuous random variable with a log-logistic distribution.
    The distribution is unimodal when ``beta > 1``.

    Explanation
    ===========

    The density of the log-logistic distribution is given by

    .. math::
        f(x) := \frac{(\frac{\beta}{\alpha})(\frac{x}{\alpha})^{\beta - 1}}
                {(1 + (\frac{x}{\alpha})^{\beta})^2}

    Parameters
    ==========

    alpha : Real number, `\alpha > 0`, scale parameter and median of distribution
    beta : Real number, `\beta > 0`, a shape parameter

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import LogLogistic, density, cdf, quantile
    >>> from sympy import Symbol, pprint

    >>> alpha = Symbol("alpha", positive=True)
    >>> beta = Symbol("beta", positive=True)
    >>> p = Symbol("p")
    >>> z = Symbol("z", positive=True)

    >>> X = LogLogistic("x", alpha, beta)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
                  beta - 1
           /  z  \
      beta*|-----|
           \alpha/
    ------------------------
                           2
          /       beta    \
          |/  z  \        |
    alpha*||-----|     + 1|
          \\alpha/        /

    >>> cdf(X)(z)
    1/(1 + (z/alpha)**(-beta))

    >>> quantile(X)(p)
    alpha*(p/(1 - p))**(1/beta)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Log-logistic_distribution

    """

    return rv(name, LogLogisticDistribution, (alpha, beta))

