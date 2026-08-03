from typing import Set

def nonlinsolve(system, *symbols):
    r"""
    Solve system of $N$ nonlinear equations with $M$ variables, which means both
    under and overdetermined systems are supported. Positive dimensional
    system is also supported (A system with infinitely many solutions is said
    to be positive-dimensional). In a positive dimensional system the solution will
    be dependent on at least one symbol. Returns both real solution
    and complex solution (if they exist).

    Parameters
    ==========

    system : list of equations
        The target system of equations
    symbols : list of Symbols
        symbols should be given as a sequence eg. list

    Returns
    =======

    A :class:`~.FiniteSet` of ordered tuple of values of `symbols` for which the `system`
    has solution. Order of values in the tuple is same as symbols present in
    the parameter `symbols`.

    Please note that general :class:`~.FiniteSet` is unordered, the solution
    returned here is not simply a :class:`~.FiniteSet` of solutions, rather it
    is a :class:`~.FiniteSet` of ordered tuple, i.e. the first and only
    argument to :class:`~.FiniteSet` is a tuple of solutions, which is
    ordered, and, hence ,the returned solution is ordered.

    Also note that solution could also have been returned as an ordered tuple,
    FiniteSet is just a wrapper ``{}`` around the tuple. It has no other
    significance except for the fact it is just used to maintain a consistent
    output format throughout the solveset.

    For the given set of equations, the respective input types
    are given below:

    .. math:: xy - 1 = 0
    .. math:: 4x^2 + y^2 - 5 = 0

    ::

       system  = [x*y - 1, 4*x**2 + y**2 - 5]
       symbols = [x, y]

    Raises
    ======

    ValueError
        The input is not valid.
        The symbols are not given.
    AttributeError
        The input symbols are not `Symbol` type.

    Examples
    ========

    >>> from sympy import symbols, nonlinsolve
    >>> x, y, z = symbols('x, y, z', real=True)
    >>> nonlinsolve([x*y - 1, 4*x**2 + y**2 - 5], [x, y])
    {(-1, -1), (-1/2, -2), (1/2, 2), (1, 1)}

    1. Positive dimensional system and complements:

    >>> from sympy import pprint
    >>> from sympy.polys.polytools import is_zero_dimensional
    >>> a, b, c, d = symbols('a, b, c, d', extended_real=True)
    >>> eq1 =  a + b + c + d
    >>> eq2 = a*b + b*c + c*d + d*a
    >>> eq3 = a*b*c + b*c*d + c*d*a + d*a*b
    >>> eq4 = a*b*c*d - 1
    >>> system = [eq1, eq2, eq3, eq4]
    >>> is_zero_dimensional(system)
    False
    >>> pprint(nonlinsolve(system, [a, b, c, d]), use_unicode=False)
      -1       1               1      -1
    {(---, -d, -, {d} \ {0}), (-, -d, ---, {d} \ {0})}
       d       d               d       d
    >>> nonlinsolve([(x+y)**2 - 4, x + y - 2], [x, y])
    {(2 - y, y)}

    2. If some of the equations are non-polynomial then `nonlinsolve`
    will call the ``substitution`` function and return real and complex solutions,
    if present.

    >>> from sympy import exp, sin
    >>> nonlinsolve([exp(x) - sin(y), y**2 - 4], [x, y])
    {(ImageSet(Lambda(_n, I*(2*_n*pi + pi) + log(sin(2))), Integers), -2),
     (ImageSet(Lambda(_n, 2*_n*I*pi + log(sin(2))), Integers), 2)}

    3. If system is non-linear polynomial and zero-dimensional then it
    returns both solution (real and complex solutions, if present) using
    :func:`~.solve_poly_system`:

    >>> from sympy import sqrt
    >>> nonlinsolve([x**2 - 2*y**2 -2, x*y - 2], [x, y])
    {(-2, -1), (2, 1), (-sqrt(2)*I, sqrt(2)*I), (sqrt(2)*I, -sqrt(2)*I)}

    4. ``nonlinsolve`` can solve some linear (zero or positive dimensional)
    system (because it uses the :func:`sympy.polys.polytools.groebner` function to get the
    groebner basis and then uses the ``substitution`` function basis as the
    new `system`). But it is not recommended to solve linear system using
    ``nonlinsolve``, because :func:`~.linsolve` is better for general linear systems.

    >>> nonlinsolve([x + 2*y -z - 3, x - y - 4*z + 9, y + z - 4], [x, y, z])
    {(3*z - 5, 4 - z, z)}

    5. System having polynomial equations and only real solution is
    solved using :func:`~.solve_poly_system`:

    >>> e1 = sqrt(x**2 + y**2) - 10
    >>> e2 = sqrt(y**2 + (-x + 10)**2) - 3
    >>> nonlinsolve((e1, e2), (x, y))
    {(191/20, -3*sqrt(391)/20), (191/20, 3*sqrt(391)/20)}
    >>> nonlinsolve([x**2 + 2/y - 2, x + y - 3], [x, y])
    {(1, 2), (1 - sqrt(5), 2 + sqrt(5)), (1 + sqrt(5), 2 - sqrt(5))}
    >>> nonlinsolve([x**2 + 2/y - 2, x + y - 3], [y, x])
    {(2, 1), (2 - sqrt(5), 1 + sqrt(5)), (2 + sqrt(5), 1 - sqrt(5))}

    6. It is better to use symbols instead of trigonometric functions or
    :class:`~.Function`. For example, replace $\sin(x)$ with a symbol, replace
    $f(x)$ with a symbol and so on. Get a solution from ``nonlinsolve`` and then
    use :func:`~.solveset` to get the value of $x$.

    How nonlinsolve is better than old solver ``_solve_system`` :
    =============================================================

    1. A positive dimensional system solver: nonlinsolve can return
    solution for positive dimensional system. It finds the
    Groebner Basis of the positive dimensional system(calling it as
    basis) then we can start solving equation(having least number of
    variable first in the basis) using solveset and substituting that
    solved solutions into other equation(of basis) to get solution in
    terms of minimum variables. Here the important thing is how we
    are substituting the known values and in which equations.

    2. Real and complex solutions: nonlinsolve returns both real
    and complex solution. If all the equations in the system are polynomial
    then using :func:`~.solve_poly_system` both real and complex solution is returned.
    If all the equations in the system are not polynomial equation then goes to
    ``substitution`` method with this polynomial and non polynomial equation(s),
    to solve for unsolved variables. Here to solve for particular variable
    solveset_real and solveset_complex is used. For both real and complex
    solution ``_solve_using_known_values`` is used inside ``substitution``
    (``substitution`` will be called when any non-polynomial equation is present).
    If a solution is valid its general solution is added to the final result.

    3. :class:`~.Complement` and :class:`~.Intersection` will be added:
    nonlinsolve maintains dict for complements and intersections. If solveset
    find complements or/and intersections with any interval or set during the
    execution of ``substitution`` function, then complement or/and
    intersection for that variable is added before returning final solution.

    """
    if not system:
        return S.EmptySet

    if not symbols:
        msg = ('Symbols must be given, for which solution of the '
               'system is to be found.')
        raise ValueError(filldedent(msg))

    if hasattr(symbols[0], '__iter__'):
        symbols = symbols[0]

    if not is_sequence(symbols) or not symbols:
        msg = ('Symbols must be given, for which solution of the '
               'system is to be found.')
        raise IndexError(filldedent(msg))

    symbols = list(map(_sympify, symbols))
    system, symbols, swap = recast_to_symbols(system, symbols)
    if swap:
        soln = nonlinsolve(system, symbols)
        return FiniteSet(*[tuple(i.xreplace(swap) for i in s) for s in soln])

    if len(system) == 1 and len(symbols) == 1:
        return _solveset_work(system, symbols)

    # main code of def nonlinsolve() starts from here

    polys, polys_expr, nonpolys, denominators, unrad_changed = \
        _separate_poly_nonpoly(system, symbols)

    poly_eqs = []
    poly_sol = [{}]

    if polys:
        poly_sol, poly_eqs = _handle_poly(polys, symbols)
        if poly_sol and poly_sol[0]:
            poly_syms = set().union(*(eq.free_symbols for eq in polys))
            unrad_syms = set().union(*(eq.free_symbols for eq in unrad_changed))
            if unrad_syms == poly_syms and unrad_changed:
                # if all the symbols have been solved by _handle_poly
                # and unrad has been used then check solutions
                poly_sol = [sol for sol in poly_sol if checksol(unrad_changed, sol)]

    # Collect together the unsolved polynomials with the non-polynomial
    # equations.
    remaining = poly_eqs + nonpolys

    # to_tuple converts a solution dictionary to a tuple containing the
    # value for each symbol
    to_tuple = lambda sol: tuple(sol[s] for s in symbols)

    if not remaining:
        # If there is nothing left to solve then return the solution from
        # solve_poly_system directly.
        return FiniteSet(*map(to_tuple, poly_sol))
    else:
        # Here we handle:
        #
        #  1. The Groebner basis if solve_poly_system failed.
        #  2. The Groebner basis in the positive-dimensional case.
        #  3. Any non-polynomial equations
        #
        # If solve_poly_system did succeed then we pass those solutions in as
        # preliminary results.
        subs_res = substitution(remaining, symbols, result=poly_sol, exclude=denominators)

        if not isinstance(subs_res, FiniteSet):
            return subs_res

        # check solutions produced by substitution. Currently, checking is done for
        # only those solutions which have non-Set variable values.
        if unrad_changed:
            result = [dict(zip(symbols, sol)) for sol in subs_res.args]
            correct_sols = [sol for sol in result if any(isinstance(v, Set) for v in sol)
                            or checksol(unrad_changed, sol) != False]
            return FiniteSet(*map(to_tuple, correct_sols))
        else:
            return subs_res

