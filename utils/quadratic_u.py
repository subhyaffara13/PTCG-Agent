
def QuadraticU(name, a, b):
    r"""
    Create a Continuous Random Variable with a U-quadratic distribution.

    Explanation
    ===========

    The density of the U-quadratic distribution is given by

    .. math::
        f(x) := \alpha (x-\beta)^2

    with :math:`x \in [a,b]`.

    Parameters
    ==========

    a : Real number
    b : Real number, :math:`a < b`

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import QuadraticU, density
    >>> from sympy import Symbol, pprint

    >>> a = Symbol("a", real=True)
    >>> b = Symbol("b", real=True)
    >>> z = Symbol("z")

    >>> X = QuadraticU("x", a, b)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
    /                2
    |   /  a   b    \
    |12*|- - - - + z|
    |   \  2   2    /
    <-----------------  for And(b >= z, a <= z)
    |            3
    |    (-a + b)
    |
    \        0                 otherwise

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/U-quadratic_distribution

    """

    return rv(name, QuadraticUDistribution, (a, b))

