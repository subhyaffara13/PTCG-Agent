
def fun_rational(t, y):
    return np.array([y[1] / t,
                     y[1] * (y[0] + 2 * y[1] - 1) / (t * (y[0] - 1))])

