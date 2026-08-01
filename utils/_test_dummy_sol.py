
def _test_dummy_sol(expected_sol,dsolve_sol):
    if type(dsolve_sol)==list:
        return any(expected_sol.dummy_eq(sub_dsol) for sub_dsol in dsolve_sol)
    else:
        return expected_sol.dummy_eq(dsolve_sol)

