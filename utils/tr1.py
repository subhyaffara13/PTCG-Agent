
def TR1(rv):
    """Replace sec, csc with 1/cos, 1/sin

    Examples
    ========

    >>> from sympy.simplify.fu import TR1, sec, csc
    >>> from sympy.abc import x
    >>> TR1(2*csc(x) + sec(x))
    1/cos(x) + 2/sin(x)
    """

    def f(rv):
        if isinstance(rv, sec):
            a = rv.args[0]
            return S.One/cos(a)
        elif isinstance(rv, csc):
            a = rv.args[0]
            return S.One/sin(a)
        return rv

    return bottom_up(rv, f)

