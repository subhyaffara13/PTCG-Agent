
def aps15_f(x, n):
    r"""piecewise linear, constant outside of [0, 0.002/(1+n)]"""
    if x < 0:
        return -0.859
    if x > 2 * 1e-3 / (1 + n):
        return np.e - 1.859
    return np.exp((n + 1) * x / 2 * 1000) - 1.859

