
def fun_rational_vectorized(t, y):
    return np.vstack((y[1] / t,
                      y[1] * (y[0] + 2 * y[1] - 1) / (t * (y[0] - 1))))

