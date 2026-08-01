
def crt1(m):
    """First part of Chinese Remainder Theorem, for multiple application.

    Examples
    ========

    >>> from sympy.ntheory.modular import crt, crt1, crt2
    >>> m = [99, 97, 95]
    >>> v = [49, 76, 65]

    The following two codes have the same result.

    >>> crt(m, v)
    (639985, 912285)

    >>> mm, e, s = crt1(m)
    >>> crt2(m, v, mm, e, s)
    (639985, 912285)

    However, it is faster when we want to fix ``m`` and
    compute for multiple ``v``, i.e. the following cases:

    >>> mm, e, s = crt1(m)
    >>> vs = [[52, 21, 37], [19, 46, 76]]
    >>> for v in vs:
    ...     print(crt2(m, v, mm, e, s))
    (397042, 912285)
    (803206, 912285)

    See Also
    ========

    sympy.polys.galoistools.gf_crt1 : low level crt routine used by this routine
    sympy.ntheory.modular.crt
    sympy.ntheory.modular.crt2

    """

    return gf_crt1(m, ZZ)

