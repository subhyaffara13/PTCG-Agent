
def check_rbf1d_stability(function):
    # Check that the Rbf function with default epsilon is not subject
    # to overshoot. Regression for issue #4523.
    #
    # Generate some data (fixed random seed hence deterministic)
    rng = np.random.RandomState(1234)
    x = np.linspace(0, 10, 50)
    z = x + 4.0 * rng.randn(len(x))

    rbf = Rbf(x, z, function=function)
    xi = np.linspace(0, 10, 1000)
    yi = rbf(xi)

    # subtract the linear trend and make sure there no spikes
    assert np.abs(yi-xi).max() / np.abs(z-x).max() < 1.1

