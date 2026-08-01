
def dup_eval(f, a, K):
    """
    Evaluate a polynomial at ``x = a`` in ``K[x]`` using Horner scheme.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_eval(x**2 + 2*x + 3, 2)
    11

    """
    if not a:
        return K.convert(dup_TC(f, K))

    result = K.zero

    for c in f:
        result *= a
        result += c

    return result

