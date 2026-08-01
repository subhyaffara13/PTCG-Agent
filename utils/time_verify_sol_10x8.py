
def time_verify_sol_10x8():
    eqs = eqs_10x8()
    sol = sol_10x8()
    zeros = [ eq.compose(sol) for eq in eqs ]
    if not all(zero == 0 for zero in zeros):
        raise ValueError("All values in zero should be 0")

