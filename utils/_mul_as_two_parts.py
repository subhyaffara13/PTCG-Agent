
def _mul_as_two_parts(f):
    """
    Find all the ways to split ``f`` into a product of two terms.
    Return None on failure.

    Explanation
    ===========

    Although the order is canonical from multiset_partitions, this is
    not necessarily the best order to process the terms. For example,
    if the case of len(gs) == 2 is removed and multiset is allowed to
    sort the terms, some tests fail.

    Examples
    ========

    >>> from sympy.integrals.meijerint import _mul_as_two_parts
    >>> from sympy import sin, exp, ordered
    >>> from sympy.abc import x
    >>> list(ordered(_mul_as_two_parts(x*sin(x)*exp(x))))
    [(x, exp(x)*sin(x)), (x*exp(x), sin(x)), (x*sin(x), exp(x))]
    """

    gs = _mul_args(f)
    if len(gs) < 2:
        return None
    if len(gs) == 2:
        return [tuple(gs)]
    return [(Mul(*x), Mul(*y)) for (x, y) in multiset_partitions(gs, 2)]

