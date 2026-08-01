
def Frechet(name, a, s=1, m=0):
    r"""
    Create a continuous random variable with a Frechet distribution.

    Explanation
    ===========

    The density of the Frechet distribution is given by

    .. math::
        f(x) := \frac{\alpha}{s} \left(\frac{x-m}{s}\right)^{-1-\alpha}
                 e^{-(\frac{x-m}{s})^{-\alpha}}

    with :math:`x \geq m`.

    Parameters
    ==========

    a : Real number, :math:`a \in \left(0, \infty\right)` the shape
    s : Real number, :math:`s \in \left(0, \infty\right)` the scale
    m : Real number, :math:`m \in \left(-\infty, \infty\right)` the minimum

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Frechet, density, cdf
    >>> from sympy import Symbol

    >>> a = Symbol("a", positive=True)
    >>> s = Symbol("s", positive=True)
    >>> m = Symbol("m", real=True)
    >>> z = Symbol("z")

    >>> X = Frechet("x", a, s, m)

    >>> density(X)(z)
    a*((-m + z)/s)**(-a - 1)*exp(-1/((-m + z)/s)**a)/s

    >>> cdf(X)(z)
    Piecewise((exp(-1/((-m + z)/s)**a), m <= z), (0, True))

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Fr%C3%A9chet_distribution

    """

    return rv(name, FrechetDistribution, (a, s, m))

