
def time_solve_lin_sys_189x49():
    eqs = eqs_189x49()
    sol = solve_lin_sys(eqs, R_49)
    if sol != sol_189x49():
        raise ValueError("Values should be equal")

