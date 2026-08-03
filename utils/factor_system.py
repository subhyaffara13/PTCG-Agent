import sys
from typing import Any

def factor_system(eqs: Sequence[Expr | complex], gens: Sequence[Expr] = (), **kwargs: Any) -> list[list[Expr]]:
    """
    Factorizes a system of polynomial equations into
    irreducible subsystems.

    Parameters
    ==========

    eqs : list
        List of expressions to be factored.
        Each expression is assumed to be equal to zero.

    gens : list, optional
        Generator(s) of the polynomial ring.
        If not provided, all free symbols will be used.

    **kwargs : dict, optional
        Same optional arguments taken by ``factor``

    Returns
    =======

    list[list[Expr]]
        A list of lists of expressions, where each sublist represents
        an irreducible subsystem. When solved, each subsystem gives
        one component of the solution. Only generic solutions are
        returned (cases not requiring parameters to be zero).

    Examples
    ========

    >>> from sympy.solvers.polysys import factor_system, factor_system_cond
    >>> from sympy.abc import x, y, a, b, c

    A simple system with multiple solutions:

    >>> factor_system([x**2 - 1, y - 1])
    [[x + 1, y - 1], [x - 1, y - 1]]

    A system with no solution:

    >>> factor_system([x, 1])
    []

    A system where any value of the symbol(s) is a solution:

    >>> factor_system([x - x, (x + 1)**2 - (x**2 + 2*x + 1)])
    [[]]

    A system with no generic solution:

    >>> factor_system([a*x*(x-1), b*y, c], [x, y])
    []

    If c is added to the unknowns then the system has a generic solution:

    >>> factor_system([a*x*(x-1), b*y, c], [x, y, c])
    [[x - 1, y, c], [x, y, c]]

    Alternatively :func:`factor_system_cond` can be used to get degenerate
    cases as well:

    >>> factor_system_cond([a*x*(x-1), b*y, c], [x, y])
    [[x - 1, y, c], [x, y, c], [x - 1, b, c], [x, b, c], [y, a, c], [a, b, c]]

    Each of the above cases is only satisfiable in the degenerate case `c = 0`.

    The solution set of the original system represented
    by eqs is the union of the solution sets of the
    factorized systems.

    An empty list [] means no generic solution exists.
    A list containing an empty list [[]] means any value of
    the symbol(s) is a solution.

    See Also
    ========

    factor_system_cond : Returns both generic and degenerate solutions
    factor_system_bool : Returns a Boolean combination representing all solutions
    sympy.polys.polytools.factor : Factors a polynomial into irreducible factors
                                   over the rational numbers
    """

    systems = _factor_system_poly_from_expr(eqs, gens, **kwargs)
    systems_generic = [sys for sys in systems if not _is_degenerate(sys)]
    systems_expr = [[p.as_expr() for p in system] for system in systems_generic]
    return systems_expr

