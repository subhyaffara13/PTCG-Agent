import sys
from typing import Any

def factor_system_bool(eqs: Sequence[Expr | complex], gens: Sequence[Expr] = (), **kwargs: Any) -> Boolean:
    """
    Factorizes a system of polynomial equations into irreducible DNF.

    The system of expressions(eqs) is taken and a Boolean combination
    of equations is returned that represents the same solution set.
    The result is in disjunctive normal form (OR of ANDs).

    Parameters
    ==========

    eqs : list
       List of expressions to be factored.
       Each expression is assumed to be equal to zero.

    gens : list, optional
       Generator(s) of the polynomial ring.
       If not provided, all free symbols will be used.

    **kwargs : dict, optional
       Optional keyword arguments


    Returns
    =======

    Boolean:
       A Boolean combination of equations. The result is typically in
       the form of a conjunction (AND) of a disjunctive normal form
       with additional conditions.

    Examples
    ========

    >>> from sympy.solvers.polysys import factor_system_bool
    >>> from sympy.abc import x, y, a, b, c
    >>> factor_system_bool([x**2 - 1])
    Eq(x - 1, 0) | Eq(x + 1, 0)

    >>> factor_system_bool([x**2 - 1, y - 1])
    (Eq(x - 1, 0) & Eq(y - 1, 0)) | (Eq(x + 1, 0) & Eq(y - 1, 0))

    >>> eqs = [a * (x - 1), b]
    >>> factor_system_bool([a*(x - 1), b])
    (Eq(a, 0) & Eq(b, 0)) | (Eq(b, 0) & Eq(x - 1, 0))

    >>> factor_system_bool([a*x**2 - a, b*(x + 1), c], [x])
    (Eq(c, 0) & Eq(x + 1, 0)) | (Eq(a, 0) & Eq(b, 0) & Eq(c, 0)) | (Eq(b, 0) & Eq(c, 0) & Eq(x - 1, 0))

    >>> factor_system_bool([x**2 + 2*x + 1 - (x + 1)**2])
    True

    The result is logically equivalent to the system of equations
    i.e. eqs. The function returns ``True`` when all values of
    the symbol(s) is a solution and ``False`` when the system
    cannot be solved.

    See Also
    ========

    factor_system : Returns factors and solvability condition separately
    factor_system_cond : Returns both factors and conditions

    """

    systems = factor_system_cond(eqs, gens, **kwargs)
    return Or(*[And(*[Eq(eq, 0) for eq in sys]) for sys in systems])

