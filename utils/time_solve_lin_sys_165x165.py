
def time_solve_lin_sys_165x165():
    eqs = eqs_165x165()
    sol = solve_lin_sys(eqs, R_165)
    if sol != sol_165x165():
        raise ValueError("Value should be equal")

