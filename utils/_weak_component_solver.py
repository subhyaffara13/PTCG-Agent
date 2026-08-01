
def _weak_component_solver(wcc, t):

    # We will divide the systems into sccs
    # only when the wcc cannot be solved as
    # a whole
    eqs = []
    for scc in wcc:
        eqs += scc
    funcs = _get_funcs_from_canon(eqs)

    sol = _strong_component_solver(eqs, funcs, t)
    if sol:
        return sol

    sol = []

    for scc in wcc:
        eqs = scc
        funcs = _get_funcs_from_canon(eqs)

        # Substituting solutions for the dependent
        # variables solved in previous SCC, if any solved.
        comp_eqs = [eq.subs({s.lhs: s.rhs for s in sol}) for eq in eqs]
        scc_sol = _strong_component_solver(comp_eqs, funcs, t)

        if scc_sol is None:
            raise NotImplementedError(filldedent('''
                The system of ODEs passed cannot be solved by dsolve_system.
            '''))

        # scc_sol: List of equations
        # scc_sol is a solution
        sol += scc_sol

    return sol

