
def test_all_bounds_equal(method):
    # this only tests methods that have parameters factored out when lb==ub
    # it does not test other methods that work with bounds
    def f(x, p1=1):
        return np.linalg.norm(x) + p1

    bounds = [(1, 1), (2, 2)]
    x0 = (1.0, 3.0)
    res = optimize.minimize(f, x0, bounds=bounds, method=method)
    assert res.success
    assert_allclose(res.fun, f([1.0, 2.0]))
    assert res.nfev == 1
    assert res.message == 'All independent variables were fixed by bounds.'

    args = (2,)
    res = optimize.minimize(f, x0, bounds=bounds, method=method, args=args)
    assert res.success
    assert_allclose(res.fun, f([1.0, 2.0], 2))

    if method.upper() == 'SLSQP':
        def con(x):
            return np.sum(x)
        nlc = NonlinearConstraint(con, -np.inf, 0.0)
        res = optimize.minimize(
            f, x0, bounds=bounds, method=method, constraints=[nlc]
        )
        assert res.success is False
        assert_allclose(res.fun, f([1.0, 2.0]))
        assert res.nfev == 1
        message = "All independent variables were fixed by bounds, but"
        assert res.message.startswith(message)

        nlc = NonlinearConstraint(con, -np.inf, 4)
        res = optimize.minimize(
            f, x0, bounds=bounds, method=method, constraints=[nlc]
        )
        assert res.success is True
        assert_allclose(res.fun, f([1.0, 2.0]))
        assert res.nfev == 1
        message = "All independent variables were fixed by bounds at values"
        assert res.message.startswith(message)

