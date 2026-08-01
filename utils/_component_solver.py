
def _component_solver(eqs, funcs, t):
    components = _component_division(eqs, funcs, t)
    sol = []

    for wcc in components:

        # wcc_sol: List of Equations
        sol += _weak_component_solver(wcc, t)

    # sol: List of Equations
    return sol

