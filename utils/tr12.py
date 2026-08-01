
def TR12(rv, first=True):
    """Separate sums in ``tan``.

    Examples
    ========

    >>> from sympy.abc import x, y
    >>> from sympy import tan
    >>> from sympy.simplify.fu import TR12
    >>> TR12(tan(x + y))
    (tan(x) + tan(y))/(-tan(x)*tan(y) + 1)
    """

    def f(rv):
        if not rv.func == tan:
            return rv

        arg = rv.args[0]
        if arg.is_Add:
            if first:
                args = list(ordered(arg.args))
            else:
                args = list(arg.args)
            a = args.pop()
            b = Add._from_args(args)
            if b.is_Add:
                tb = TR12(tan(b), first=False)
            else:
                tb = tan(b)
            return (tan(a) + tb)/(1 - tan(a)*tb)
        return rv

    return bottom_up(rv, f)

