
def test_onesided_bounded_powell_stability():
    # When the Powell method is bounded on only one side, a
    # np.tan transform is done in order to convert it into a
    # completely bounded problem. Here we do some simple tests
    # of one-sided bounded Powell where the optimal solutions
    # are large to test the stability of the transformation.
    kwargs = {'method': 'Powell',
              'bounds': [(-np.inf, 1e6)] * 3,
              'options': {'ftol': 1e-8, 'xtol': 1e-8}}
    x0 = [1, 1, 1]

    # df/dx is constant.
    def f(x):
        return -np.sum(x)
    res = optimize.minimize(f, x0, **kwargs)
    assert_allclose(res.fun, -3e6, atol=1e-4)

    # df/dx gets smaller and smaller.
    def f(x):
        return -np.abs(np.sum(x)) ** (0.1) * (1 if np.all(x > 0) else -1)

    res = optimize.minimize(f, x0, **kwargs)
    assert_allclose(res.fun, -(3e6) ** (0.1))

    # df/dx gets larger and larger.
    def f(x):
        return -np.abs(np.sum(x)) ** 10 * (1 if np.all(x > 0) else -1)

    res = optimize.minimize(f, x0, **kwargs)
    assert_allclose(res.fun, -(3e6) ** 10, rtol=1e-7)

    # df/dx gets larger for some of the variables and smaller for others.
    def f(x):
        t = -np.abs(np.sum(x[:2])) ** 5 - np.abs(np.sum(x[2:])) ** (0.1)
        t *= (1 if np.all(x > 0) else -1)
        return t

    kwargs['bounds'] = [(-np.inf, 1e3)] * 3
    res = optimize.minimize(f, x0, **kwargs)
    assert_allclose(res.fun, -(2e3) ** 5 - (1e6) ** (0.1), rtol=1e-7)

