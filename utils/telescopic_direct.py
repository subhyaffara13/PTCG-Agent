
def telescopic_direct(L, R, n, limits):
    """
    Returns the direct summation of the terms of a telescopic sum

    Explanation
    ===========

    L is the term with lower index
    R is the term with higher index
    n difference between the indexes of L and R

    Examples
    ========

    >>> from sympy.concrete.summations import telescopic_direct
    >>> from sympy.abc import k, a, b
    >>> telescopic_direct(1/k, -1/(k+2), 2, (k, a, b))
    -1/(b + 2) - 1/(b + 1) + 1/(a + 1) + 1/a

    """
    (i, a, b) = limits
    return Add(*[L.subs(i, a + m) + R.subs(i, b - m) for m in range(n)])

