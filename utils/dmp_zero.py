
def dmp_zero(u):
    """
    Return a multivariate zero.

    Examples
    ========

    >>> from sympy.polys.densebasic import dmp_zero

    >>> dmp_zero(4)
    [[[[[]]]]]

    """
    r = []

    for i in range(u):
        r = [r]

    return r

