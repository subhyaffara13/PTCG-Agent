
def factor_sum(self, limits=None, radical=False, clear=False, fraction=False, sign=True):
    """Return Sum with constant factors extracted.

    If ``limits`` is specified then ``self`` is the summand; the other
    keywords are passed to ``factor_terms``.

    Examples
    ========

    >>> from sympy import Sum
    >>> from sympy.abc import x, y
    >>> from sympy.simplify.simplify import factor_sum
    >>> s = Sum(x*y, (x, 1, 3))
    >>> factor_sum(s)
    y*Sum(x, (x, 1, 3))
    >>> factor_sum(s.function, s.limits)
    y*Sum(x, (x, 1, 3))
    """

    # XXX deprecate in favor of direct call to factor_terms
    kwargs = {"radical": radical, "clear": clear,
        "fraction": fraction, "sign": sign}
    expr = Sum(self, *limits) if limits else self
    return factor_terms(expr, **kwargs)

