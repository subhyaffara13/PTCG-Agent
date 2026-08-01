
def test_zero_interval(method):
    # Case where upper and lower limits of integration are the same
    # Result of integration should match initial state.
    # f[y(t)] = 2y(t)
    def f(t, y):
        return 2 * y
    res = solve_ivp(f, (0.0, 0.0), np.array([1.0]), method=method)
    assert res.success
    assert_allclose(res.y[0, -1], 1.0)

