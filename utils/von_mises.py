
def VonMises(name, mu, k):
    r"""
    Create a Continuous Random Variable with a von Mises distribution.

    Explanation
    ===========

    The density of the von Mises distribution is given by

    .. math::
        f(x) := \frac{e^{\kappa\cos(x-\mu)}}{2\pi I_0(\kappa)}

    with :math:`x \in [0,2\pi]`.

    Parameters
    ==========

    mu : Real number
        Measure of location.
    k : Real number
        Measure of concentration.

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import VonMises, density
    >>> from sympy import Symbol, pprint

    >>> mu = Symbol("mu")
    >>> k = Symbol("k", positive=True)
    >>> z = Symbol("z")

    >>> X = VonMises("x", mu, k)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
         k*cos(mu - z)
        e
    ------------------
    2*pi*besseli(0, k)


    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Von_Mises_distribution
    .. [2] https://mathworld.wolfram.com/vonMisesDistribution.html

    """

    return rv(name, VonMisesDistribution, (mu, k))

