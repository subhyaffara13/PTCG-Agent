
def dup_clear_denoms(f, K0, K1=None, convert=False):
    """
    Clear denominators, i.e. transform ``K_0`` to ``K_1``.

    Examples
    ========

    >>> from sympy.polys import ring, QQ
    >>> R, x = ring("x", QQ)

    >>> f = QQ(1,2)*x + QQ(1,3)

    >>> R.dup_clear_denoms(f, convert=False)
    (6, 3*x + 2)
    >>> R.dup_clear_denoms(f, convert=True)
    (6, 3*x + 2)

    """
    if K1 is None:
        if K0.has_assoc_Ring:
            K1 = K0.get_ring()
        else:
            K1 = K0

    common = K1.one

    for c in f:
        common = K1.lcm(common, K0.denom(c))

    if K1.is_one(common):
        if not convert:
            return common, f
        else:
            return common, dup_convert(f, K0, K1)

    # Use quo rather than exquo to handle inexact domains by discarding the
    # remainder.
    f = [K0.numer(c)*K1.quo(common, K0.denom(c)) for c in f]

    if not convert:
        return common, dup_convert(f, K1, K0)
    else:
        return common, f

