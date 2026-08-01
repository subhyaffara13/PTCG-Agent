
def big_sol(x, n):
    y = np.ones((2 * n, x.size))
    y[::2] = x
    return x

