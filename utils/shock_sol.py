
def shock_sol(x):
    eps = 1e-3
    k = np.sqrt(2 * eps)
    return np.cos(np.pi * x) + erf(x / k) / erf(1 / k)

