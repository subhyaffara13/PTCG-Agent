
def base_solution_linear(c, a, b, t=None):
    """
    Return the base solution for the linear equation, `ax + by = c`.

    Explanation
    ===========

    Used by ``diop_linear()`` to find the base solution of a linear
    Diophantine equation. If ``t`` is given then the parametrized solution is
    returned.

    Usage
    =====

    ``base_solution_linear(c, a, b, t)``: ``a``, ``b``, ``c`` are coefficients
    in `ax + by = c` and ``t`` is the parameter to be used in the solution.

    Examples
    ========

    >>> from sympy.solvers.diophantine.diophantine import base_solution_linear
    >>> from sympy.abc import t
    >>> base_solution_linear(5, 2, 3) # equation 2*x + 3*y = 5
    (-5, 5)
    >>> base_solution_linear(0, 5, 7) # equation 5*x + 7*y = 0
    (0, 0)
    >>> base_solution_linear(5, 2, 3, t) # equation 2*x + 3*y = 5
    (3*t - 5, 5 - 2*t)
    >>> base_solution_linear(0, 5, 7, t) # equation 5*x + 7*y = 0
    (7*t, -5*t)
    """
    a, b, c = _remove_gcd(a, b, c)

    if c == 0:
        if t is None:
            return (0, 0)
        if b < 0:
            t = -t
        return (b*t, -a*t)

    x0, y0, d = igcdex(abs(a), abs(b))
    x0 *= sign(a)
    y0 *= sign(b)
    if c % d:
        return (None, None)
    if t is None:
        return (c*x0, c*y0)
    if b < 0:
        t = -t
    return (c*x0 + b*t, c*y0 - a*t)

