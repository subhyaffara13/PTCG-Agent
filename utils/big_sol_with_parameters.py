
def big_sol_with_parameters(x, p):
    # big version of sl_sol, with two parameters
    return np.vstack((np.sin(p[0] * x), np.sin(p[1] * x)))

