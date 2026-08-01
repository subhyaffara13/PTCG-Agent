
def diop_ternary_quadratic_normal(eq, parameterize=False):
    """
    Solves the quadratic ternary diophantine equation,
    `ax^2 + by^2 + cz^2 = 0`.

    Explanation
    ===========

    Here the coefficients `a`, `b`, and `c` should be non zero. Otherwise the
    equation will be a quadratic binary or univariate equation. If solvable,
    returns a tuple `(x, y, z)` that satisfies the given equation. If the
    equation does not have integer solutions, `(None, None, None)` is returned.

    Usage
    =====

    ``diop_ternary_quadratic_normal(eq)``: where ``eq`` is an equation of the form
    `ax^2 + by^2 + cz^2 = 0`.

    Examples
    ========

    >>> from sympy.abc import x, y, z
    >>> from sympy.solvers.diophantine.diophantine import diop_ternary_quadratic_normal
    >>> diop_ternary_quadratic_normal(x**2 + 3*y**2 - z**2)
    (1, 0, 1)
    >>> diop_ternary_quadratic_normal(4*x**2 + 5*y**2 - z**2)
    (1, 0, 2)
    >>> diop_ternary_quadratic_normal(34*x**2 - 3*y**2 - 301*z**2)
    (4, 9, 1)
    """
    var, coeff, diop_type = classify_diop(eq, _dict=False)
    if diop_type == HomogeneousTernaryQuadraticNormal.name:
        sol = _diop_ternary_quadratic_normal(var, coeff)
        if len(sol) > 0:
            x_0, y_0, z_0 = list(sol)[0]
        else:
            x_0, y_0, z_0 = None, None, None
        if parameterize:
            return _parametrize_ternary_quadratic(
                (x_0, y_0, z_0), var, coeff)
        return x_0, y_0, z_0

