
def time_solve_lin_sys_10x8():
    eqs = eqs_10x8()
    sol = solve_lin_sys(eqs, R_8)
    if sol != sol_10x8():
        raise ValueError("Values should be equal")

