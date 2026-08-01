
def RaisedCosine(name, mu, s):
    r"""
    Create a Continuous Random Variable with a raised cosine distribution.

    Explanation
    ===========

    The density of the raised cosine distribution is given by

    .. math::
        f(x) := \frac{1}{2s}\left(1+\cos\left(\frac{x-\mu}{s}\pi\right)\right)

    with :math:`x \in [\mu-s,\mu+s]`.

    Parameters
    ==========

    mu : Real number
    s : Real number, `s > 0`

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import RaisedCosine, density
    >>> from sympy import Symbol, pprint

    >>> mu = Symbol("mu", real=True)
    >>> s = Symbol("s", positive=True)
    >>> z = Symbol("z")

    >>> X = RaisedCosine("x", mu, s)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
    /   /pi*(-mu + z)\
    |cos|------------| + 1
    |   \     s      /
    <---------------------  for And(z >= mu - s, z <= mu + s)
    |         2*s
    |
    \          0                        otherwise

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Raised_cosine_distribution

    """

    return rv(name, RaisedCosineDistribution, (mu, s))

