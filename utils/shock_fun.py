
def shock_fun(x, y):
    eps = 1e-3
    return np.vstack((
        y[1],
        -(x * y[1] + eps * np.pi**2 * np.cos(np.pi * x) +
          np.pi * x * np.sin(np.pi * x)) / eps
    ))

