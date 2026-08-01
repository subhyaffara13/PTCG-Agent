
def laplace_initial_conds(f, t, fdict, /):
    """
    This helper function takes a function `f` that is the result of a
    ``laplace_transform``.  It takes an fdict of the form ``{y: [1, 4, 2]}``,
    where the values in the list are the initial value, the initial slope, the
    initial second derivative, etc., of the function `y(t)`, and replaces all
    unevaluated initial conditions.

    Parameters
    ==========

    f : sympy expression
        Expression containing initial conditions of unevaluated functions.
    t : sympy expression
        Variable for which the initial conditions are to be applied.
    fdict : dictionary
        Dictionary containing a list of initial conditions for every
        function, e.g., ``{y: [0, 1, 2], x: [3, 4, 5]}``. The order
        of derivatives is ascending, so `0`, `1`, `2` are `y(0)`, `y'(0)`,
        and `y''(0)`, respectively.

    Examples
    ========

    >>> from sympy import laplace_transform, diff, Function
    >>> from sympy import laplace_correspondence, laplace_initial_conds
    >>> from sympy.abc import t, s
    >>> y = Function("y")
    >>> Y = Function("Y")
    >>> f = laplace_transform(diff(y(t), t, 3), t, s, noconds=True)
    >>> g = laplace_correspondence(f, {y: Y})
    >>> laplace_initial_conds(g, t, {y: [2, 4, 8, 16, 32]})
    s**3*Y(s) - 2*s**2 - 4*s - 8
    """
    for y, ic in fdict.items():
        for k in range(len(ic)):
            if k == 0:
                f = f.replace(y(0), ic[0])
            elif k == 1:
                f = f.replace(Subs(Derivative(y(t), t), t, 0), ic[1])
            else:
                f = f.replace(Subs(Derivative(y(t), (t, k)), t, 0), ic[k])
    return f

