
def pspace(expr):
    """
    Returns the underlying Probability Space of a random expression.

    For internal use.

    Examples
    ========

    >>> from sympy.stats import pspace, Normal
    >>> X = Normal('X', 0, 1)
    >>> pspace(2*X + 1) == X.pspace
    True
    """
    expr = sympify(expr)
    if isinstance(expr, RandomSymbol) and expr.pspace is not None:
        return expr.pspace
    if expr.has(RandomMatrixSymbol):
        rm = list(expr.atoms(RandomMatrixSymbol))[0]
        return rm.pspace

    rvs = random_symbols(expr)
    if not rvs:
        raise ValueError("Expression containing Random Variable expected, not %s" % (expr))
    # If only one space present
    if all(rv.pspace == rvs[0].pspace for rv in rvs):
        return rvs[0].pspace
    from sympy.stats.compound_rv import CompoundPSpace
    from sympy.stats.stochastic_process import StochasticPSpace
    for rv in rvs:
        if isinstance(rv.pspace, (CompoundPSpace, StochasticPSpace)):
            return rv.pspace
    # Otherwise make a product space
    return IndependentProductPSpace(*[rv.pspace for rv in rvs])

