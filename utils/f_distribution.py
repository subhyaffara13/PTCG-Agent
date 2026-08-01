
def FDistribution(name, d1, d2):
    r"""
    Create a continuous random variable with a F distribution.

    Explanation
    ===========

    The density of the F distribution is given by

    .. math::
        f(x) := \frac{\sqrt{\frac{(d_1 x)^{d_1} d_2^{d_2}}
                {(d_1 x + d_2)^{d_1 + d_2}}}}
                {x \mathrm{B} \left(\frac{d_1}{2}, \frac{d_2}{2}\right)}

    with :math:`x > 0`.

    Parameters
    ==========

    d1 : `d_1 > 0`, where `d_1` is the degrees of freedom (`n_1 - 1`)
    d2 : `d_2 > 0`, where `d_2` is the degrees of freedom (`n_2 - 1`)

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import FDistribution, density
    >>> from sympy import Symbol, pprint

    >>> d1 = Symbol("d1", positive=True)
    >>> d2 = Symbol("d2", positive=True)
    >>> z = Symbol("z")

    >>> X = FDistribution("x", d1, d2)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
      d2
      --    ______________________________
      2    /       d1            -d1 - d2
    d2  *\/  (d1*z)  *(d1*z + d2)
    --------------------------------------
                    /d1  d2\
                 z*B|--, --|
                    \2   2 /

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/F-distribution
    .. [2] https://mathworld.wolfram.com/F-Distribution.html

    """

    return rv(name, FDistributionDistribution, (d1, d2))

