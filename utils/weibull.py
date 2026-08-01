
def Weibull(name, alpha, beta):
    r"""
    Create a continuous random variable with a Weibull distribution.

    Explanation
    ===========

    The density of the Weibull distribution is given by

    .. math::
        f(x) := \begin{cases}
                  \frac{k}{\lambda}\left(\frac{x}{\lambda}\right)^{k-1}
                  e^{-(x/\lambda)^{k}} & x\geq0\\
                  0 & x<0
                \end{cases}

    Parameters
    ==========

    lambda : Real number, $\lambda > 0$, a scale
    k : Real number, $k > 0$, a shape

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Weibull, density, E, variance
    >>> from sympy import Symbol, simplify

    >>> l = Symbol("lambda", positive=True)
    >>> k = Symbol("k", positive=True)
    >>> z = Symbol("z")

    >>> X = Weibull("x", l, k)

    >>> density(X)(z)
    k*(z/lambda)**(k - 1)*exp(-(z/lambda)**k)/lambda

    >>> simplify(E(X))
    lambda*gamma(1 + 1/k)

    >>> simplify(variance(X))
    lambda**2*(-gamma(1 + 1/k)**2 + gamma(1 + 2/k))

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Weibull_distribution
    .. [2] https://mathworld.wolfram.com/WeibullDistribution.html

    """

    return rv(name, WeibullDistribution, (alpha, beta))

