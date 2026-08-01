
def test_bounded_powell_vs_powell():
    # here we test an example where the bounded Powell method
    # will return a different result than the standard Powell
    # method.

    # first we test a simple example where the minimum is at
    # the origin and the minimum that is within the bounds is
    # larger than the minimum at the origin.
    def func(x):
        return np.sum(x ** 2)
    bounds = (-5, -1), (-10, -0.1), (1, 9.2), (-4, 7.6), (-15.9, -2)
    x0 = [-2.1, -5.2, 1.9, 0, -2]

    options = {'ftol': 1e-10, 'xtol': 1e-10}

    res_powell = optimize.minimize(func, x0, method="Powell", options=options)
    assert_allclose(res_powell.x, 0., atol=1e-6)
    assert_allclose(res_powell.fun, 0., atol=1e-6)

    res_bounded_powell = optimize.minimize(func, x0, options=options,
                                           bounds=bounds,
                                           method="Powell")
    p = np.array([-1, -0.1, 1, 0, -2])
    assert_allclose(res_bounded_powell.x, p, atol=1e-6)
    assert_allclose(res_bounded_powell.fun, func(p), atol=1e-6)

    # now we test bounded Powell but with a mix of inf bounds.
    bounds = (None, -1), (-np.inf, -.1), (1, np.inf), (-4, None), (-15.9, -2)
    res_bounded_powell = optimize.minimize(func, x0, options=options,
                                           bounds=bounds,
                                           method="Powell")
    p = np.array([-1, -0.1, 1, 0, -2])
    assert_allclose(res_bounded_powell.x, p, atol=1e-6)
    assert_allclose(res_bounded_powell.fun, func(p), atol=1e-6)

    # next we test an example where the global minimum is within
    # the bounds, but the bounded Powell method performs better
    # than the standard Powell method.
    def func(x):
        t = np.sin(-x[0]) * np.cos(x[1]) * np.sin(-x[0] * x[1]) * np.cos(x[1])
        t -= np.cos(np.sin(x[1] * x[2]) * np.cos(x[2]))
        return t**2

    bounds = [(-2, 5)] * 3
    x0 = [-0.5, -0.5, -0.5]

    res_powell = optimize.minimize(func, x0, method="Powell")
    res_bounded_powell = optimize.minimize(func, x0,
                                           bounds=bounds,
                                           method="Powell")
    assert_allclose(res_powell.fun, 0.007136253919761627, atol=1e-6)
    assert_allclose(res_bounded_powell.fun, 0, atol=1e-6)

    # next we test the previous example where the we provide Powell
    # with (-inf, inf) bounds, and compare it to providing Powell
    # with no bounds. They should end up the same.
    bounds = [(-np.inf, np.inf)] * 3

    res_bounded_powell = optimize.minimize(func, x0,
                                           bounds=bounds,
                                           method="Powell")
    assert_allclose(res_powell.fun, res_bounded_powell.fun, atol=1e-6)
    assert_allclose(res_powell.nfev, res_bounded_powell.nfev, atol=1e-6)
    assert_allclose(res_powell.x, res_bounded_powell.x, atol=1e-6)

    # now test when x0 starts outside of the bounds.
    x0 = [45.46254415, -26.52351498, 31.74830248]
    bounds = [(-2, 5)] * 3
    # we're starting outside the bounds, so we should get a warning
    with pytest.warns(optimize.OptimizeWarning):
        res_bounded_powell = optimize.minimize(func, x0,
                                               bounds=bounds,
                                               method="Powell")
    assert_allclose(res_bounded_powell.fun, 0, atol=1e-6)

