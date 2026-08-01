
def checkpdesol(pde, sol, func=None, solve_for_func=True):
    """
    Checks if the given solution satisfies the partial differential
    equation.

    pde is the partial differential equation which can be given in the
    form of an equation or an expression. sol is the solution for which
    the pde is to be checked. This can also be given in an equation or
    an expression form. If the function is not provided, the helper
    function _preprocess from deutils is used to identify the function.

    If a sequence of solutions is passed, the same sort of container will be
    used to return the result for each solution.

    The following methods are currently being implemented to check if the
    solution satisfies the PDE:

        1. Directly substitute the solution in the PDE and check. If the
           solution has not been solved for f, then it will solve for f
           provided solve_for_func has not been set to False.

    If the solution satisfies the PDE, then a tuple (True, 0) is returned.
    Otherwise a tuple (False, expr) where expr is the value obtained
    after substituting the solution in the PDE. However if a known solution
    returns False, it may be due to the inability of doit() to simplify it to zero.

    Examples
    ========

    >>> from sympy import Function, symbols
    >>> from sympy.solvers.pde import checkpdesol, pdsolve
    >>> x, y = symbols('x y')
    >>> f = Function('f')
    >>> eq = 2*f(x,y) + 3*f(x,y).diff(x) + 4*f(x,y).diff(y)
    >>> sol = pdsolve(eq)
    >>> assert checkpdesol(eq, sol)[0]
    >>> eq = x*f(x,y) + f(x,y).diff(x)
    >>> checkpdesol(eq, sol)
    (False, (x*F(4*x - 3*y) - 6*F(4*x - 3*y)/25 + 4*Subs(Derivative(F(_xi_1), _xi_1), _xi_1, 4*x - 3*y))*exp(-6*x/25 - 8*y/25))
    """

    # Converting the pde into an equation
    if not isinstance(pde, Equality):
        pde = Eq(pde, 0)

    # If no function is given, try finding the function present.
    if func is None:
        try:
            _, func = _preprocess(pde.lhs)
        except ValueError:
            funcs = [s.atoms(AppliedUndef) for s in (
                sol if is_sequence(sol, set) else [sol])]
            funcs = set().union(funcs)
            if len(funcs) != 1:
                raise ValueError(
                    'must pass func arg to checkpdesol for this case.')
            func = funcs.pop()

    # If the given solution is in the form of a list or a set
    # then return a list or set of tuples.
    if is_sequence(sol, set):
        return type(sol)([checkpdesol(
            pde, i, func=func,
            solve_for_func=solve_for_func) for i in sol])

    # Convert solution into an equation
    if not isinstance(sol, Equality):
        sol = Eq(func, sol)
    elif sol.rhs == func:
        sol = sol.reversed

    # Try solving for the function
    solved = sol.lhs == func and not sol.rhs.has(func)
    if solve_for_func and not solved:
        solved = solve(sol, func)
        if solved:
            if len(solved) == 1:
                return checkpdesol(pde, Eq(func, solved[0]),
                    func=func, solve_for_func=False)
            else:
                return checkpdesol(pde, [Eq(func, t) for t in solved],
                    func=func, solve_for_func=False)

    # try direct substitution of the solution into the PDE and simplify
    if sol.lhs == func:
        pde = pde.lhs - pde.rhs
        s = simplify(pde.subs(func, sol.rhs).doit())
        return s is S.Zero, s

    raise NotImplementedError(filldedent('''
        Unable to test if %s is a solution to %s.''' % (sol, pde)))

