
def _is_special_case_of(soln1, soln2, eq, order, var):
    r"""
    True if soln1 is found to be a special case of soln2 wrt some value of the
    constants that appear in soln2. False otherwise.
    """
    # The solutions returned by dsolve may be given explicitly or implicitly.
    # We will equate the sol1=(soln1.rhs - soln1.lhs), sol2=(soln2.rhs - soln2.lhs)
    # of the two solutions.
    #
    # Since this is supposed to hold for all x it also holds for derivatives.
    # For an order n ode we should be able to differentiate
    # each solution n times to get n+1 equations.
    #
    # We then try to solve those n+1 equations for the integrations constants
    # in sol2. If we can find a solution that does not depend on x then it
    # means that some value of the constants in sol1 is a special case of
    # sol2 corresponding to a particular choice of the integration constants.

    # In case the solution is in implicit form we subtract the sides
    soln1 = soln1.rhs - soln1.lhs
    soln2 = soln2.rhs - soln2.lhs

    # Work for the series solution
    if soln1.has(Order) and soln2.has(Order):
        if soln1.getO() == soln2.getO():
            soln1 = soln1.removeO()
            soln2 = soln2.removeO()
        else:
            return False
    elif soln1.has(Order) or soln2.has(Order):
        return False

    constants1 = soln1.free_symbols.difference(eq.free_symbols)
    constants2 = soln2.free_symbols.difference(eq.free_symbols)

    constants1_new = get_numbered_constants(Tuple(soln1, soln2), len(constants1))
    if len(constants1) == 1:
        constants1_new = {constants1_new}
    for c_old, c_new in zip(constants1, constants1_new):
        soln1 = soln1.subs(c_old, c_new)

    # n equations for sol1 = sol2, sol1'=sol2', ...
    lhs = soln1
    rhs = soln2
    eqns = [Eq(lhs, rhs)]
    for n in range(1, order):
        lhs = lhs.diff(var)
        rhs = rhs.diff(var)
        eq = Eq(lhs, rhs)
        eqns.append(eq)

    # BooleanTrue/False awkwardly show up for trivial equations
    if any(isinstance(eq, BooleanFalse) for eq in eqns):
        return False
    eqns = [eq for eq in eqns if not isinstance(eq, BooleanTrue)]

    try:
        constant_solns = solve(eqns, constants2)
    except NotImplementedError:
        return False

    # Sometimes returns a dict and sometimes a list of dicts
    if isinstance(constant_solns, dict):
        constant_solns = [constant_solns]

    # after solving the issue 17418, maybe we don't need the following checksol code.
    for constant_soln in constant_solns:
        for eq in eqns:
            eq=eq.rhs-eq.lhs
            if checksol(eq, constant_soln) is not True:
                return False

    # If any solution gives all constants as expressions that don't depend on
    # x then there exists constants for soln2 that give soln1
    for constant_soln in constant_solns:
        if not any(c.has(var) for c in constant_soln.values()):
            return True

    return False

