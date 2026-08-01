
def time_verify_sol_189x49():
    eqs = eqs_189x49()
    sol = sol_189x49()
    zeros = [ eq.compose(sol) for eq in eqs ]
    assert all(zero == 0 for zero in zeros)

