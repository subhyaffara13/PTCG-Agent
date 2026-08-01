
def BoundedPareto(name, alpha, left, right):
    r"""
    Create a continuous random variable with a Bounded Pareto distribution.

    The density of the Bounded Pareto distribution is given by

    .. math::
        f(x) := \frac{\alpha L^{\alpha}x^{-\alpha-1}}{1-(\frac{L}{H})^{\alpha}}

    Parameters
    ==========

    alpha : Real Number, `\alpha > 0`
        Shape parameter
    left : Real Number, `left > 0`
        Location parameter
    right : Real Number, `right > left`
        Location parameter

    Examples
    ========

    >>> from sympy.stats import BoundedPareto, density, cdf, E
    >>> from sympy import symbols
    >>> L, H = symbols('L, H', positive=True)
    >>> X = BoundedPareto('X', 2, L, H)
    >>> x = symbols('x')
    >>> density(X)(x)
    2*L**2/(x**3*(1 - L**2/H**2))
    >>> cdf(X)(x)
    Piecewise((-H**2*L**2/(x**2*(H**2 - L**2)) + H**2/(H**2 - L**2), L <= x), (0, True))
    >>> E(X).simplify()
    2*H*L/(H + L)

    Returns
    =======

    RandomSymbol

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Pareto_distribution#Bounded_Pareto_distribution

    """
    return rv (name, BoundedParetoDistribution, (alpha, left, right))

