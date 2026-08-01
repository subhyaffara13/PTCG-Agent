
def LogitNormal(name, mu, s):
    r"""
    Create a continuous random variable with a Logit-Normal distribution.

    The density of the logistic distribution is given by

    .. math::
        f(x) := \frac{1}{s \sqrt{2 \pi}} \frac{1}{x(1 - x)} e^{- \frac{(logit(x)  - \mu)^2}{s^2}}
        where logit(x) = \log(\frac{x}{1 - x})
    Parameters
    ==========

    mu : Real number, the location (mean)
    s : Real number, `s > 0`, a scale

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import LogitNormal, density, cdf
    >>> from sympy import Symbol,pprint

    >>> mu = Symbol("mu", real=True)
    >>> s = Symbol("s", positive=True)
    >>> z = Symbol("z")
    >>> X = LogitNormal("x",mu,s)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
                              2
            /         /  z  \\
           -|-mu + log|-----||
            \         \1 - z//
           ---------------------
                       2
      ___           2*s
    \/ 2 *e
    ----------------------------
            ____
        2*\/ pi *s*z*(1 - z)

    >>> density(X)(z)
    sqrt(2)*exp(-(-mu + log(z/(1 - z)))**2/(2*s**2))/(2*sqrt(pi)*s*z*(1 - z))

    >>> cdf(X)(z)
    erf(sqrt(2)*(-mu + log(z/(1 - z)))/(2*s))/2 + 1/2


    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Logit-normal_distribution

    """

    return rv(name, LogitNormalDistribution, (mu, s))

