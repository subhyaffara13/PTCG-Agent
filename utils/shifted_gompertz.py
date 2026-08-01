
def ShiftedGompertz(name, b, eta):
    r"""
    Create a continuous random variable with a Shifted Gompertz distribution.

    Explanation
    ===========

    The density of the Shifted Gompertz distribution is given by

    .. math::
        f(x) := b e^{-b x} e^{-\eta \exp(-b x)} \left[1 + \eta(1 - e^(-bx)) \right]

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
    >>> from sympy.stats import ShiftedGompertz, density
    >>> from sympy import Symbol

    >>> b = Symbol("b", positive=True)
    >>> eta = Symbol("eta", positive=True)
    >>> x = Symbol("x")

    >>> X = ShiftedGompertz("x", b, eta)

    >>> density(X)(x)
    b*(eta*(1 - exp(-b*x)) + 1)*exp(-b*x)*exp(-eta*exp(-b*x))

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Shifted_Gompertz_distribution

    """
    return rv(name, ShiftedGompertzDistribution, (b, eta))

