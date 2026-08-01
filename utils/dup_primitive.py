
def dup_primitive(f, K):
    """
    Compute content and the primitive form of ``f`` in ``K[x]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ, QQ

    >>> R, x = ring("x", ZZ)
    >>> f = 6*x**2 + 8*x + 12

    >>> R.dup_primitive(f)
    (2, 3*x**2 + 4*x + 6)

    >>> R, x = ring("x", QQ)
    >>> f = 6*x**2 + 8*x + 12

    >>> R.dup_primitive(f)
    (2, 3*x**2 + 4*x + 6)

    """
    if not f:
        return K.zero, f

    cont = dup_content(f, K)

    if K.is_one(cont):
        return cont, f
    else:
        return cont, dup_quo_ground(f, cont, K)

