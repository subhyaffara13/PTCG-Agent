
def stiff_f(t, y):
    return np.array([
        y[0],
        -0.04 * y[1] + 1e4 * y[2] * y[3],
        0.04 * y[1] - 1e4 * y[2] * y[3] - 3e7 * y[2]**2,
        3e7 * y[2]**2,
        y[4]
    ])

