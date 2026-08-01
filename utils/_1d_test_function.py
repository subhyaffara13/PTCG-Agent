
def _1d_test_function(x, xp):
    # Test function used in Wahba's "Spline Models for Observational Data".
    # domain ~= (0, 3), range ~= (-1.0, 0.2)
    x = x[:, 0]
    y = 4.26*(xp.exp(-x) - 4*xp.exp(-2*x) + 3*xp.exp(-3*x))
    return y

