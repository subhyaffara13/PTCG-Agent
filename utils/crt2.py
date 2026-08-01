
def crt2(m, v, mm, e, s, symmetric=False):
    """Second part of Chinese Remainder Theorem, for multiple application.

    See ``crt1`` for usage.

    Examples
    ========

    >>> from sympy.ntheory.modular import crt1, crt2
    >>> mm, e, s = crt1([18, 42, 6])
    >>> crt2([18, 42, 6], [0, 0, 0], mm, e, s)
    (0, 4536)

    See Also
    ========

    sympy.polys.galoistools.gf_crt2 : low level crt routine used by this routine
    sympy.ntheory.modular.crt
    sympy.ntheory.modular.crt1

    """

    result = gf_crt2(v, m, mm, e, s, ZZ)

    if symmetric:
        return int(symmetric_residue(result, mm)), int(mm)
    return int(result), int(mm)

