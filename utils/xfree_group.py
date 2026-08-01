
def xfree_group(symbols):
    """Construct a free group returning ``(FreeGroup, (f_0, f_1, ..., f_(n-1)))``.

    Parameters
    ==========

    symbols : str, Symbol/Expr or sequence of str, Symbol/Expr (may be empty)

    Examples
    ========

    >>> from sympy.combinatorics.free_groups import xfree_group
    >>> F, (x, y, z) = xfree_group("x, y, z")
    >>> F
    <free group on the generators (x, y, z)>
    >>> y**2*x**-2*z**-1
    y**2*x**-2*z**-1
    >>> type(_)
    <class 'sympy.combinatorics.free_groups.FreeGroupElement'>

    """
    _free_group = FreeGroup(symbols)
    return (_free_group, _free_group.generators)

