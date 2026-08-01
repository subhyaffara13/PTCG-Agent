
def expand_trig(expr, deep=True):
    """
    Wrapper around expand that only uses the trig hint.  See the expand
    docstring for more information.

    Examples
    ========

    >>> from sympy import expand_trig, sin
    >>> from sympy.abc import x, y
    >>> expand_trig(sin(x+y)*(x+y))
    (x + y)*(sin(x)*cos(y) + sin(y)*cos(x))

    """
    return sympify(expr).expand(deep=deep, trig=True, basic=False,
    log=False, mul=False, power_exp=False, power_base=False, multinomial=False)

