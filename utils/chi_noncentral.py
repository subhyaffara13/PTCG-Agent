
def ChiNoncentral(name, k, l):
    r"""
    Create a continuous random variable with a non-central Chi distribution.

    Explanation
    ===========

    The density of the non-central Chi distribution is given by

    .. math::
        f(x) := \frac{e^{-(x^2+\lambda^2)/2} x^k\lambda}
                {(\lambda x)^{k/2}} I_{k/2-1}(\lambda x)

    with `x \geq 0`. Here, `I_\nu (x)` is the
    :ref:`modified Bessel function of the first kind <besseli>`.

    Parameters
    ==========

    k : A positive Integer, $k > 0$
        The number of degrees of freedom.
    lambda : Real number, `\lambda > 0`
        Shift parameter.

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import ChiNoncentral, density
    >>> from sympy import Symbol

    >>> k = Symbol("k", integer=True)
    >>> l = Symbol("l")
    >>> z = Symbol("z")

    >>> X = ChiNoncentral("x", k, l)

    >>> density(X)(z)
    l*z**k*exp(-l**2/2 - z**2/2)*besseli(k/2 - 1, l*z)/(l*z)**(k/2)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Noncentral_chi_distribution
    """

    return rv(name, ChiNoncentralDistribution, (k, l))

