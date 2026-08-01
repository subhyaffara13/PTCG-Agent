
def factor_system_cond(eqs: Sequence[Expr | complex], gens: Sequence[Expr] = (), **kwargs: Any) -> list[list[Expr]]:
    """
    Factorizes a polynomial system into irreducible components and returns
    both generic and degenerate solutions.

    Parameters
    ==========

    eqs : list
        List of expressions to be factored.
        Each expression is assumed to be equal to zero.

    gens : list, optional
        Generator(s) of the polynomial ring.
        If not provided, all free symbols will be used.

    **kwargs : dict, optional
        Optional keyword arguments.

    Returns
    =======

    list[list[Expr]]
        A list of lists of expressions, where each sublist represents
        an irreducible subsystem. Includes both generic solutions and
        degenerate cases requiring equality conditions on parameters.

    Examples
    ========

    >>> from sympy.solvers.polysys import factor_system_cond
    >>> from sympy.abc import x, y, a, b, c

    >>> factor_system_cond([x**2 - 4, a*y, b], [x, y])
    [[x + 2, y, b], [x - 2, y, b], [x + 2, a, b], [x - 2, a, b]]

    >>> factor_system_cond([a*x*(x-1), b*y, c], [x, y])
    [[x - 1, y, c], [x, y, c], [x - 1, b, c], [x, b, c], [y, a, c], [a, b, c]]

    An empty list [] means no solution exists.
    A list containing an empty list [[]] means any value of
    the symbol(s) is a solution.

    See Also
    ========

    factor_system : Returns only generic solutions
    factor_system_bool : Returns a Boolean combination representing all solutions
    sympy.polys.polytools.factor : Factors a polynomial into irreducible factors
                                   over the rational numbers
    """
    systems_poly = _factor_system_poly_from_expr(eqs, gens, **kwargs)
    systems = [[p.as_expr() for p in system] for system in systems_poly]
    return systems

