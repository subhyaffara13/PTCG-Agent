
def iterargs(expr):
    """Yield the args of a Basic object in a breadth-first traversal.
    Depth-traversal stops if `arg.args` is either empty or is not
    an iterable.

    Examples
    ========

    >>> from sympy import Integral, Function
    >>> from sympy.abc import x
    >>> f = Function('f')
    >>> from sympy.core.traversal import iterargs
    >>> list(iterargs(Integral(f(x), (f(x), 1))))
    [Integral(f(x), (f(x), 1)), f(x), (f(x), 1), x, f(x), 1, x]

    See Also
    ========
    iterfreeargs, preorder_traversal
    """
    args = [expr]
    for i in args:
        yield i
        args.extend(i.args)

