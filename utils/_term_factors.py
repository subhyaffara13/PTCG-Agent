
def _term_factors(f):
    """
    Iterator to get the factors of all terms present
    in the given equation.

    Parameters
    ==========
    f : Expr
        Equation that needs to be addressed

    Returns
    =======
    Factors of all terms present in the equation.

    Examples
    ========

    >>> from sympy import symbols
    >>> from sympy.solvers.solveset import _term_factors
    >>> x = symbols('x')
    >>> list(_term_factors(-2 - x**2 + x*(x + 1)))
    [-2, -1, x**2, x, x + 1]
    """
    for add_arg in Add.make_args(f):
        yield from Mul.make_args(add_arg)

