
def diop_linear(eq, param=symbols("t", integer=True)):
    """
    Solves linear diophantine equations.

    A linear diophantine equation is an equation of the form `a_{1}x_{1} +
    a_{2}x_{2} + .. + a_{n}x_{n} = 0` where `a_{1}, a_{2}, ..a_{n}` are
    integer constants and `x_{1}, x_{2}, ..x_{n}` are integer variables.

    Usage
    =====

    ``diop_linear(eq)``: Returns a tuple containing solutions to the
    diophantine equation ``eq``. Values in the tuple is arranged in the same
    order as the sorted variables.

    Details
    =======

    ``eq`` is a linear diophantine equation which is assumed to be zero.
    ``param`` is the parameter to be used in the solution.

    Examples
    ========

    >>> from sympy.solvers.diophantine.diophantine import diop_linear
    >>> from sympy.abc import x, y, z
    >>> diop_linear(2*x - 3*y - 5) # solves equation 2*x - 3*y - 5 == 0
    (3*t_0 - 5, 2*t_0 - 5)

    Here x = -3*t_0 - 5 and y = -2*t_0 - 5

    >>> diop_linear(2*x - 3*y - 4*z -3)
    (t_0, 2*t_0 + 4*t_1 + 3, -t_0 - 3*t_1 - 3)

    See Also
    ========

    diop_quadratic(), diop_ternary_quadratic(), diop_general_pythagorean(),
    diop_general_sum_of_squares()
    """
    var, coeff, diop_type = classify_diop(eq, _dict=False)

    if diop_type == Linear.name:
        parameters = None
        if param is not None:
            parameters = symbols('%s_0:%i' % (param, len(var)), integer=True)

        result = Linear(eq).solve(parameters=parameters)

        if param is None:
            result = result(*[0]*len(result.parameters))

        if len(result) > 0:
            return list(result)[0]
        else:
            return tuple([None]*len(result.parameters))

