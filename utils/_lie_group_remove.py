
def _lie_group_remove(coords):
    r"""
    This function is strictly meant for internal use by the Lie group ODE solving
    method. It replaces arbitrary functions returned by pdsolve as follows:

    1] If coords is an arbitrary function, then its argument is returned.
    2] An arbitrary function in an Add object is replaced by zero.
    3] An arbitrary function in a Mul object is replaced by one.
    4] If there is no arbitrary function coords is returned unchanged.

    Examples
    ========

    >>> from sympy.solvers.ode.lie_group import _lie_group_remove
    >>> from sympy import Function
    >>> from sympy.abc import x, y
    >>> F = Function("F")
    >>> eq = x**2*y
    >>> _lie_group_remove(eq)
    x**2*y
    >>> eq = F(x**2*y)
    >>> _lie_group_remove(eq)
    x**2*y
    >>> eq = x*y**2 + F(x**3)
    >>> _lie_group_remove(eq)
    x*y**2
    >>> eq = (F(x**3) + y)*x**4
    >>> _lie_group_remove(eq)
    x**4*y

    """
    if isinstance(coords, AppliedUndef):
        return coords.args[0]
    elif coords.is_Add:
        subfunc = coords.atoms(AppliedUndef)
        if subfunc:
            for func in subfunc:
                coords = coords.subs(func, 0)
        return coords
    elif coords.is_Pow:
        base, expr = coords.as_base_exp()
        base = _lie_group_remove(base)
        expr = _lie_group_remove(expr)
        return base**expr
    elif coords.is_Mul:
        mulargs = []
        coordargs = coords.args
        for arg in coordargs:
            if not isinstance(coords, AppliedUndef):
                mulargs.append(_lie_group_remove(arg))
        return Mul(*mulargs)
    return coords

