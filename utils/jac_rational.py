
def jac_rational(t, y):
    return np.array([
        [0, 1 / t],
        [-2 * y[1] ** 2 / (t * (y[0] - 1) ** 2),
         (y[0] + 4 * y[1] - 1) / (t * (y[0] - 1))]
    ])

