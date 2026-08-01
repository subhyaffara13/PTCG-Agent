
def TR7(rv):
    """Lowering the degree of cos(x)**2.

    Examples
    ========

    >>> from sympy.simplify.fu import TR7
    >>> from sympy.abc import x
    >>> from sympy import cos
    >>> TR7(cos(x)**2)
    cos(2*x)/2 + 1/2
    >>> TR7(cos(x)**2 + 1)
    cos(2*x)/2 + 3/2

    """

    def f(rv):
        if not (rv.is_Pow and rv.base.func == cos and rv.exp == 2):
            return rv
        return (1 + cos(2*rv.base.args[0]))/2

    return bottom_up(rv, f)

