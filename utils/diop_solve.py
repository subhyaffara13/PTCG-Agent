
def diop_solve(eq, param=symbols("t", integer=True)):
    """
    Solves the diophantine equation ``eq``.

    Explanation
    ===========

    Unlike ``diophantine()``, factoring of ``eq`` is not attempted. Uses
    ``classify_diop()`` to determine the type of the equation and calls
    the appropriate solver function.

    Use of ``diophantine()`` is recommended over other helper functions.
    ``diop_solve()`` can return either a set or a tuple depending on the
    nature of the equation. All non-trivial solutions are returned: assumptions
    on symbols are ignored.

    Usage
    =====

    ``diop_solve(eq, t)``: Solve diophantine equation, ``eq`` using ``t``
    as a parameter if needed.

    Details
    =======

    ``eq`` should be an expression which is assumed to be zero.
    ``t`` is a parameter to be used in the solution.

    Examples
    ========

    >>> from sympy.solvers.diophantine import diop_solve
    >>> from sympy.abc import x, y, z, w
    >>> diop_solve(2*x + 3*y - 5)
    (3*t_0 - 5, 5 - 2*t_0)
    >>> diop_solve(4*x + 3*y - 4*z + 5)
    (t_0, 8*t_0 + 4*t_1 + 5, 7*t_0 + 3*t_1 + 5)
    >>> diop_solve(x + 3*y - 4*z + w - 6)
    (t_0, t_0 + t_1, 6*t_0 + 5*t_1 + 4*t_2 - 6, 5*t_0 + 4*t_1 + 3*t_2 - 6)
    >>> diop_solve(x**2 + y**2 - 5)
    {(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)}


    See Also
    ========

    diophantine()
    """
    var, coeff, eq_type = classify_diop(eq, _dict=False)

    if eq_type == Linear.name:
        return diop_linear(eq, param)

    elif eq_type == BinaryQuadratic.name:
        return diop_quadratic(eq, param)

    elif eq_type == HomogeneousTernaryQuadratic.name:
        return diop_ternary_quadratic(eq, parameterize=True)

    elif eq_type == HomogeneousTernaryQuadraticNormal.name:
        return diop_ternary_quadratic_normal(eq, parameterize=True)

    elif eq_type == GeneralPythagorean.name:
        return diop_general_pythagorean(eq, param)

    elif eq_type == Univariate.name:
        return diop_univariate(eq)

    elif eq_type == GeneralSumOfSquares.name:
        return diop_general_sum_of_squares(eq, limit=S.Infinity)

    elif eq_type == GeneralSumOfEvenPowers.name:
        return diop_general_sum_of_even_powers(eq, limit=S.Infinity)

    if eq_type is not None and eq_type not in diop_known:
            raise ValueError(filldedent('''
    Although this type of equation was identified, it is not yet
    handled. It should, however, be listed in `diop_known` at the
    top of this file. Developers should see comments at the end of
    `classify_diop`.
            '''))  # pragma: no cover
    else:
        raise NotImplementedError(
            'No solver has been written for %s.' % eq_type)

