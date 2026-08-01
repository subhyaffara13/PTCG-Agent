
def ExponentialPower(name, mu, alpha, beta):
    r"""
    Create a Continuous Random Variable with Exponential Power distribution.
    This distribution is known also as Generalized Normal
    distribution version 1.

    Explanation
    ===========

    The density of the Exponential Power distribution is given by

    .. math::
        f(x) := \frac{\beta}{2\alpha\Gamma(\frac{1}{\beta})}
            e^{{-(\frac{|x - \mu|}{\alpha})^{\beta}}}

    with :math:`x \in [ - \infty, \infty ]`.

    Parameters
    ==========

    mu : Real number
        A location.
    alpha : Real number,`\alpha > 0`
        A  scale.
    beta : Real number, `\beta > 0`
        A shape.

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import ExponentialPower, density, cdf
    >>> from sympy import Symbol, pprint
    >>> z = Symbol("z")
    >>> mu = Symbol("mu")
    >>> alpha = Symbol("alpha", positive=True)
    >>> beta = Symbol("beta", positive=True)
    >>> X = ExponentialPower("x", mu, alpha, beta)
    >>> pprint(density(X)(z), use_unicode=False)
                     beta
           /|mu - z|\
          -|--------|
           \ alpha  /
    beta*e
    ---------------------
                  / 1  \
     2*alpha*Gamma|----|
                  \beta/
    >>> cdf(X)(z)
    1/2 + lowergamma(1/beta, (Abs(mu - z)/alpha)**beta)*sign(-mu + z)/(2*gamma(1/beta))

    References
    ==========

    .. [1] https://reference.wolfram.com/language/ref/ExponentialPowerDistribution.html
    .. [2] https://en.wikipedia.org/wiki/Generalized_normal_distribution#Version_1

    """
    return rv(name, ExponentialPowerDistribution, (mu, alpha, beta))

