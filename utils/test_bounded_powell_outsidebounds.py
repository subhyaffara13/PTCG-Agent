
def test_bounded_powell_outsidebounds():
    # With the bounded Powell method if you start outside the bounds the final
    # should still be within the bounds (provided that the user doesn't make a
    # bad choice for the `direc` argument).
    def func(x):
        return np.sum(x ** 2)
    bounds = (-1, 1), (-1, 1), (-1, 1)
    x0 = [-4, .5, -.8]

    # we're starting outside the bounds, so we should get a warning
    with pytest.warns(optimize.OptimizeWarning):
        res = optimize.minimize(func, x0, bounds=bounds, method="Powell")
    assert_allclose(res.x, np.array([0.] * len(x0)), atol=1e-6)
    assert_equal(res.success, True)
    assert_equal(res.status, 0)

    # However, now if we change the `direc` argument such that the
    # set of vectors does not span the parameter space, then we may
    # not end up back within the bounds. Here we see that the first
    # parameter cannot be updated!
    direc = [[0, 0, 0], [0, 1, 0], [0, 0, 1]]
    # we're starting outside the bounds, so we should get a warning
    with pytest.warns(optimize.OptimizeWarning):
        res = optimize.minimize(func, x0,
                                bounds=bounds, method="Powell",
                                options={'direc': direc})
    assert_allclose(res.x, np.array([-4., 0, 0]), atol=1e-6)
    assert_equal(res.success, False)
    assert_equal(res.status, 4)

