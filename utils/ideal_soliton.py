
def IdealSoliton(name, k):
    r"""
    Create a Finite Random Variable of Ideal Soliton Distribution

    Parameters
    ==========

    k : Positive Integer
        Represents the number of input symbols in an LT (Luby Transform) code.

    Examples
    ========

    >>> from sympy.stats import IdealSoliton, density, P, E
    >>> sol = IdealSoliton('sol', 5)
    >>> density(sol).dict
    {1: 1/5, 2: 1/2, 3: 1/6, 4: 1/12, 5: 1/20}
    >>> density(sol).set
    {1, 2, 3, 4, 5}

    >>> from sympy import Symbol
    >>> k = Symbol('k', positive=True, integer=True)
    >>> sol = IdealSoliton('sol', k)
    >>> density(sol).dict
    Density(IdealSolitonDistribution(k))
    >>> density(sol).dict.subs(k, 10).doit()
    {1: 1/10, 2: 1/2, 3: 1/6, 4: 1/12, 5: 1/20, 6: 1/30, 7: 1/42, 8: 1/56, 9: 1/72, 10: 1/90}

    >>> E(sol.subs(k, 10))
    7381/2520

    >>> P(sol.subs(k, 4) > 2)
    1/4

    Returns
    =======

    RandomSymbol

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Soliton_distribution#Ideal_distribution
    .. [2] https://pages.cs.wisc.edu/~suman/courses/740/papers/luby02lt.pdf

    """
    return rv(name, IdealSolitonDistribution, k)

