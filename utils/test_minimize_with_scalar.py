
def test_minimize_with_scalar(method):
    # checks that minimize works with a scalar being provided to it.
    def f(x):
        return np.sum(x ** 2)

    res = optimize.minimize(f, 17, bounds=[(-100, 100)], method=method)
    assert res.success
    assert_allclose(res.x, [0.0], atol=1e-5)

