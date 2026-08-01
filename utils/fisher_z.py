
def FisherZ(name, d1, d2):
    r"""
    Create a Continuous Random Variable with an Fisher's Z distribution.

    Explanation
    ===========

    The density of the Fisher's Z distribution is given by

    .. math::
        f(x) := \frac{2d_1^{d_1/2} d_2^{d_2/2}} {\mathrm{B}(d_1/2, d_2/2)}
                \frac{e^{d_1z}}{\left(d_1e^{2z}+d_2\right)^{\left(d_1+d_2\right)/2}}


    .. TODO - What is the difference between these degrees of freedom?

    Parameters
    ==========

    d1 : `d_1 > 0`
        Degree of freedom.
    d2 : `d_2 > 0`
        Degree of freedom.

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import FisherZ, density
    >>> from sympy import Symbol, pprint

    >>> d1 = Symbol("d1", positive=True)
    >>> d2 = Symbol("d2", positive=True)
    >>> z = Symbol("z")

    >>> X = FisherZ("x", d1, d2)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
                                d1   d2
        d1   d2               - -- - --
        --   --                 2    2
        2    2  /    2*z     \           d1*z
    2*d1  *d2  *\d1*e    + d2/         *e
    -----------------------------------------
                     /d1  d2\
                    B|--, --|
                     \2   2 /

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Fisher%27s_z-distribution
    .. [2] https://mathworld.wolfram.com/Fishersz-Distribution.html

    """

    return rv(name, FisherZDistribution, (d1, d2))

