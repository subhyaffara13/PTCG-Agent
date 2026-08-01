
def nonlin_bc_fun(x, y):
    # laplace eq.
    return np.stack([y[1], np.zeros_like(x)])

