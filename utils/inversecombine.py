
def inversecombine(expr):
    """Simplify the composition of a function and its inverse.

    Explanation
    ===========

    No attention is paid to whether the inverse is a left inverse or a
    right inverse; thus, the result will in general not be equivalent
    to the original expression.

    Examples
    ========

    >>> from sympy.simplify.simplify import inversecombine
    >>> from sympy import asin, sin, log, exp
    >>> from sympy.abc import x
    >>> inversecombine(asin(sin(x)))
    x
    >>> inversecombine(2*log(exp(3*x)))
    6*x
    """

    def f(rv):
        if isinstance(rv, log):
            if isinstance(rv.args[0], exp) or (rv.args[0].is_Pow and rv.args[0].base == S.Exp1):
                rv = rv.args[0].exp
        elif rv.is_Function and hasattr(rv, "inverse"):
            if (len(rv.args) == 1 and len(rv.args[0].args) == 1 and
               isinstance(rv.args[0], rv.inverse(argindex=1))):
                rv = rv.args[0].args[0]
        if rv.is_Pow and rv.base == S.Exp1:
            if isinstance(rv.exp, log):
                rv = rv.exp.args[0]
        return rv

    return _bottom_up(expr, f)

