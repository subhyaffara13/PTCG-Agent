
def sdm_LT(f):
    r"""
    Returns the leading term of ``f``.

    Only valid if `f \ne 0`.

    Examples
    ========

    >>> from sympy.polys.distributedmodules import sdm_LT, sdm_from_dict
    >>> from sympy.polys import QQ, lex
    >>> dic = {(1, 2, 3): QQ(1), (4, 0, 0): QQ(2), (4, 0, 1): QQ(3)}
    >>> sdm_LT(sdm_from_dict(dic, lex))
    ((4, 0, 1), 3)
    """
    return f[0]

