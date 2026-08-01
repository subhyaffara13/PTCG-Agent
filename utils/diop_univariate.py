
def diop_univariate(eq):
    """
    Solves a univariate diophantine equations.

    Explanation
    ===========

    A univariate diophantine equation is an equation of the form
    `a_{0} + a_{1}x + a_{2}x^2 + .. + a_{n}x^n = 0` where `a_{1}, a_{2}, ..a_{n}` are
    integer constants and `x` is an integer variable.

    Usage
    =====

    ``diop_univariate(eq)``: Returns a set containing solutions to the
    diophantine equation ``eq``.

    Details
    =======

    ``eq`` is a univariate diophantine equation which is assumed to be zero.

    Examples
    ========

    >>> from sympy.solvers.diophantine.diophantine import diop_univariate
    >>> from sympy.abc import x
    >>> diop_univariate((x - 2)*(x - 3)**2) # solves equation (x - 2)*(x - 3)**2 == 0
    {(2,), (3,)}

    """
    var, coeff, diop_type = classify_diop(eq, _dict=False)

    if diop_type == Univariate.name:
        return {(int(i),) for i in solveset_real(
            eq, var[0]).intersect(S.Integers)}

