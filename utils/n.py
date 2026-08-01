
def N(x, n=15, **options):
    r"""
    Calls x.evalf(n, \*\*options).

    Explanations
    ============

    Both .n() and N() are equivalent to .evalf(); use the one that you like better.
    See also the docstring of .evalf() for information on the options.

    Examples
    ========

    >>> from sympy import Sum, oo, N
    >>> from sympy.abc import k
    >>> Sum(1/k**k, (k, 1, oo))
    Sum(k**(-k), (k, 1, oo))
    >>> N(_, 4)
    1.291

    """
    # by using rational=True, any evaluation of a string
    # will be done using exact values for the Floats
    return sympify(x, rational=True).evalf(n, **options)


def n():
    return 100

