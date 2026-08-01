
def test_check_grad():
    # Verify if check_grad is able to estimate the derivative of the
    # expit (logistic sigmoid) function.

    def expit(x):
        return 1 / (1 + np.exp(-x))

    def der_expit(x):
        return np.exp(-x) / (1 + np.exp(-x))**2

    x0 = np.array([1.5])

    r = optimize.check_grad(expit, der_expit, x0)
    assert_almost_equal(r, 0)
    # SPEC-007 leave one call with seed to check it still works
    r = optimize.check_grad(expit, der_expit, x0,
                            direction='random', seed=1234)
    assert_almost_equal(r, 0)

    r = optimize.check_grad(expit, der_expit, x0, epsilon=1e-6)
    assert_almost_equal(r, 0)
    r = optimize.check_grad(expit, der_expit, x0, epsilon=1e-6,
                            direction='random', rng=1234)
    assert_almost_equal(r, 0)

    # Check if the epsilon parameter is being considered.
    r = abs(optimize.check_grad(expit, der_expit, x0, epsilon=1e-1) - 0)
    assert r > 1e-7
    r = abs(optimize.check_grad(expit, der_expit, x0, epsilon=1e-1,
                                direction='random', rng=1234) - 0)
    assert r > 1e-7

    def x_sinx(x):
        return (x*np.sin(x)).sum()

    def der_x_sinx(x):
        return np.sin(x) + x*np.cos(x)

    x0 = np.arange(0, 2, 0.2)

    r = optimize.check_grad(x_sinx, der_x_sinx, x0,
                            direction='random', rng=1234)
    assert_almost_equal(r, 0)

    assert_raises(ValueError, optimize.check_grad,
                  x_sinx, der_x_sinx, x0,
                  direction='random_projection', rng=1234)

    # checking can be done for derivatives of vector valued functions
    r = optimize.check_grad(himmelblau_grad, himmelblau_hess, himmelblau_x0,
                            direction='all', rng=1234)
    assert r < 5e-7

