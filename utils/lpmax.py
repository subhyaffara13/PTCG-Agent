
def lpmax(f, constr):
    """return maximum of linear equation ``f`` under
    linear constraints expressed using Ge, Le or Eq.

    All variables are unbounded unless constrained.

    Examples
    ========

    >>> from sympy.solvers.simplex import lpmax
    >>> from sympy import Eq
    >>> from sympy.abc import x, y
    >>> lpmax(x, [2*x - 3*y >= -1, Eq(x+ 3*y,2), x <= 2*y])
    (4/5, {x: 4/5, y: 2/5})

    Negative values for variables are permitted unless explicitly
    excluding:

    >>> lpmax(x, [x <= -1])
    (-1, {x: -1})

    If a non-negative constraint is added for x, there is no
    possible solution:

    >>> lpmax(x, [x <= -1, x >= 0])
    Traceback (most recent call last):
    ...
    sympy.solvers.simplex.InfeasibleLPError: inconsistent/False constraint

    See Also
    ========
    linprog, lpmin
    """
    return _lp(max, f, constr)

