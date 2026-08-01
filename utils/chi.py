
def Chi(name, k):
    r"""
    Create a continuous random variable with a Chi distribution.

    The density of the Chi distribution is given by

    .. math::
        f(x) := \frac{2^{1-k/2}x^{k-1}e^{-x^2/2}}{\Gamma(k/2)}

    with :math:`x \geq 0`.

    Parameters
    ==========

    k : Positive integer, The number of degrees of freedom

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Chi, density, E
    >>> from sympy import Symbol, simplify

    >>> k = Symbol("k", integer=True)
    >>> z = Symbol("z")

    >>> X = Chi("x", k)

    >>> density(X)(z)
    2**(1 - k/2)*z**(k - 1)*exp(-z**2/2)/gamma(k/2)

    >>> simplify(E(X))
    sqrt(2)*gamma(k/2 + 1/2)/gamma(k/2)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Chi_distribution
    .. [2] https://mathworld.wolfram.com/ChiDistribution.html

    """

    return rv(name, ChiDistribution, (k,))


def chi(ctx, z):
    nz = ctx.fneg(z, exact=True)
    v = 0.5*(ctx.ei(z) + ctx.ei(nz))
    zreal = ctx._re(z)
    zimag = ctx._im(z)
    if zimag > 0:
        v += ctx.pi*0.5j
    elif zimag < 0:
        v -= ctx.pi*0.5j
    elif zreal < 0:
        v += ctx.pi*1j
    return v

