
def BetaNoncentral(name, alpha, beta, lamda):
    r"""
    Create a Continuous Random Variable with a Type I Noncentral Beta distribution.

    The density of the Noncentral Beta distribution is given by

    .. math::
        f(x) := \sum_{k=0}^\infty e^{-\lambda/2}\frac{(\lambda/2)^k}{k!}
                \frac{x^{\alpha+k-1}(1-x)^{\beta-1}}{\mathrm{B}(\alpha+k,\beta)}

    with :math:`x \in [0,1]`.

    Parameters
    ==========

    alpha : Real number, `\alpha > 0`, a shape
    beta : Real number, `\beta > 0`, a shape
    lamda : Real number, `\lambda \geq 0`, noncentrality parameter

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import BetaNoncentral, density, cdf
    >>> from sympy import Symbol, pprint

    >>> alpha = Symbol("alpha", positive=True)
    >>> beta = Symbol("beta", positive=True)
    >>> lamda = Symbol("lamda", nonnegative=True)
    >>> z = Symbol("z")

    >>> X = BetaNoncentral("x", alpha, beta, lamda)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
      oo
    _____
    \    `
     \                                              -lamda
      \                          k                  -------
       \    k + alpha - 1 /lamda\         beta - 1     2
        )  z             *|-----| *(1 - z)        *e
       /                  \  2  /
      /    ------------------------------------------------
     /                  B(k + alpha, beta)*k!
    /____,
    k = 0

    Compute cdf with specific 'x', 'alpha', 'beta' and 'lamda' values as follows:

    >>> cdf(BetaNoncentral("x", 1, 1, 1), evaluate=False)(2).doit()
    2*exp(1/2)

    The argument evaluate=False prevents an attempt at evaluation
    of the sum for general x, before the argument 2 is passed.

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Noncentral_beta_distribution
    .. [2] https://reference.wolfram.com/language/ref/NoncentralBetaDistribution.html

    """

    return rv(name, BetaNoncentralDistribution, (alpha, beta, lamda))

