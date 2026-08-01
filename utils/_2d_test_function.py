
def _2d_test_function(x, xp):
    # Franke's test function.
    # domain ~= (0, 1) X (0, 1), range ~= (0.0, 1.2)
    x1, x2 = x[:, 0], x[:, 1]
    term1 = 0.75 * xp.exp(-(9*x1-2)**2/4 - (9*x2-2)**2/4)
    term2 = 0.75 * xp.exp(-(9*x1+1)**2/49 - (9*x2+1)/10)
    term3 = 0.5 * xp.exp(-(9*x1-7)**2/4 - (9*x2-3)**2/4)
    term4 = -0.2 * xp.exp(-(9*x1-4)**2 - (9*x2-7)**2)
    y = term1 + term2 + term3 + term4
    return y

