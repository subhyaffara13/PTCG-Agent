
def _strong_component_solver(eqs, funcs, t):
    from sympy.solvers.ode.ode import dsolve, constant_renumber

    match = _classify_linear_system(eqs, funcs, t, is_canon=True)
    sol = None

    # Assuming that we can't get an implicit system
    # since we are already canonical equations from
    # dsolve_system
    if match:
        match['t'] = t

        if match.get('is_higher_order', False):
            sol = _higher_order_ode_solver(match)

        elif match.get('is_linear', False):
            sol = _linear_ode_solver(match)

        # Note: For now, only linear systems are handled by this function
        # hence, the match condition is added. This can be removed later.
        if sol is None and len(eqs) == 1:
            sol = dsolve(eqs[0], func=funcs[0])
            variables = Tuple(eqs[0]).free_symbols
            new_constants = [Dummy() for _ in range(ode_order(eqs[0], funcs[0]))]
            sol = constant_renumber(sol, variables=variables, newconstants=new_constants)
            sol = [sol]

        # To add non-linear case here in future

    return sol

