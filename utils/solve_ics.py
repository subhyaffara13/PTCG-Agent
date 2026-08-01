
def solve_ics(sols, funcs, constants, ics):
    """
    Solve for the constants given initial conditions

    ``sols`` is a list of solutions.

    ``funcs`` is a list of functions.

    ``constants`` is a list of constants.

    ``ics`` is the set of initial/boundary conditions for the differential
    equation. It should be given in the form of ``{f(x0): x1,
    f(x).diff(x).subs(x, x2):  x3}`` and so on.

    Returns a dictionary mapping constants to values.
    ``solution.subs(constants)`` will replace the constants in ``solution``.

    Example
    =======
    >>> # From dsolve(f(x).diff(x) - f(x), f(x))
    >>> from sympy import symbols, Eq, exp, Function
    >>> from sympy.solvers.ode.ode import solve_ics
    >>> f = Function('f')
    >>> x, C1 = symbols('x C1')
    >>> sols = [Eq(f(x), C1*exp(x))]
    >>> funcs = [f(x)]
    >>> constants = [C1]
    >>> ics = {f(0): 2}
    >>> solved_constants = solve_ics(sols, funcs, constants, ics)
    >>> solved_constants
    {C1: 2}
    >>> sols[0].subs(solved_constants)
    Eq(f(x), 2*exp(x))

    """
    # Assume ics are of the form f(x0): value or Subs(diff(f(x), x, n), (x,
    # x0)): value (currently checked by classify_ode). To solve, replace x
    # with x0, f(x0) with value, then solve for constants. For f^(n)(x0),
    # differentiate the solution n times, so that f^(n)(x) appears.
    x = funcs[0].args[0]
    diff_sols = []
    subs_sols = []
    diff_variables = set()
    for funcarg, value in ics.items():
        if isinstance(funcarg, AppliedUndef):
            x0 = funcarg.args[0]
            matching_func = [f for f in funcs if f.func == funcarg.func][0]
            S = sols
        elif isinstance(funcarg, (Subs, Derivative)):
            if isinstance(funcarg, Subs):
                # Make sure it stays a subs. Otherwise subs below will produce
                # a different looking term.
                funcarg = funcarg.doit()
            if isinstance(funcarg, Subs):
                deriv = funcarg.expr
                x0 = funcarg.point[0]
                variables = funcarg.expr.variables
                matching_func = deriv
            elif isinstance(funcarg, Derivative):
                deriv = funcarg
                x0 = funcarg.variables[0]
                variables = (x,)*len(funcarg.variables)
                matching_func = deriv.subs(x0, x)
            for sol in sols:
                if sol.has(deriv.expr.func):
                    diff_sols.append(Eq(sol.lhs.diff(*variables), sol.rhs.diff(*variables)))
            diff_variables.add(variables)
            S = diff_sols
        else:
            raise NotImplementedError("Unrecognized initial condition")

        for sol in S:
            if sol.has(matching_func):
                sol2 = sol
                sol2 = sol2.subs(x, x0)
                sol2 = sol2.subs(funcarg, value)
                # This check is necessary because of issue #15724
                if not isinstance(sol2, BooleanAtom) or not subs_sols:
                    subs_sols = [s for s in subs_sols if not isinstance(s, BooleanAtom)]
                    subs_sols.append(sol2)

    # TODO: Use solveset here
    try:
        solved_constants = solve(subs_sols, constants, dict=True)
    except NotImplementedError:
        solved_constants = []

    # XXX: We can't differentiate between the solution not existing because of
    # invalid initial conditions, and not existing because solve is not smart
    # enough. If we could use solveset, this might be improvable, but for now,
    # we use NotImplementedError in this case.
    if not solved_constants:
        raise ValueError("Couldn't solve for initial conditions")

    if solved_constants == True:
        raise ValueError("Initial conditions did not produce any solutions for constants. Perhaps they are degenerate.")

    if len(solved_constants) > 1:
        raise NotImplementedError("Initial conditions produced too many solutions for constants")

    return solved_constants[0]

