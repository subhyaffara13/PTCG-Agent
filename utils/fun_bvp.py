
def fun_bvp(x):
    n = int(np.sqrt(x.shape[0]))
    u = np.zeros((n + 2, n + 2))
    x = x.reshape((n, n))
    u[1:-1, 1:-1] = x
    y = u[:-2, 1:-1] + u[2:, 1:-1] + u[1:-1, :-2] + u[1:-1, 2:] - 4 * x + x**3
    return y.ravel()

