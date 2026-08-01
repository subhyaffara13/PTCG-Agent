
def ContinuousRV(symbol, density, set=Interval(-oo, oo), **kwargs):
    """
    Create a Continuous Random Variable given the following:

    Parameters
    ==========

    symbol : Symbol
        Represents name of the random variable.
    density : Expression containing symbol
        Represents probability density function.
    set : set/Interval
        Represents the region where the pdf is valid, by default is real line.
    check : bool
        If True, it will check whether the given density
        integrates to 1 over the given set. If False, it
        will not perform this check. Default is False.


    Returns
    =======

    RandomSymbol

    Many common continuous random variable types are already implemented.
    This function should be necessary only very rarely.


    Examples
    ========

    >>> from sympy import Symbol, sqrt, exp, pi
    >>> from sympy.stats import ContinuousRV, P, E

    >>> x = Symbol("x")

    >>> pdf = sqrt(2)*exp(-x**2/2)/(2*sqrt(pi)) # Normal distribution
    >>> X = ContinuousRV(x, pdf)

    >>> E(X)
    0
    >>> P(X>0)
    1/2
    """
    pdf = Piecewise((density, set.as_relational(symbol)), (0, True))
    pdf = Lambda(symbol, pdf)
    # have a default of False while `rv` should have a default of True
    kwargs['check'] = kwargs.pop('check', False)
    return rv(symbol.name, ContinuousDistributionHandmade, (pdf, set), **kwargs)

