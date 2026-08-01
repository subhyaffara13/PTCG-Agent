
def Gompertz(name, b, eta):
    r"""
    Create a Continuous Random Variable with Gompertz distribution.

    Explanation
    ===========

    The density of the Gompertz distribution is given by

    .. math::
        f(x) := b \eta e^{b x} e^{\eta} \exp \left(-\eta e^{bx} \right)

    with :math:`x \in [0, \infty)`.

    Parameters
    ==========

    b : Real number, `b > 0`, a scale
    eta : Real number, `\eta > 0`, a shape

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Gompertz, density
    >>> from sympy import Symbol

    >>> b = Symbol("b", positive=True)
    >>> eta = Symbol("eta", positive=True)
    >>> z = Symbol("z")

    >>> X = Gompertz("x", b, eta)

    >>> density(X)(z)
    b*eta*exp(eta)*exp(b*z)*exp(-eta*exp(b*z))

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Gompertz_distribution

    """
    return rv(name, GompertzDistribution, (b, eta))

