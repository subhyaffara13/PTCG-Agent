
def test_minimize_multiple_constraints():
    # Regression test for gh-4240.
    def func(x):
        return np.array([25 - 0.2 * x[0] - 0.4 * x[1] - 0.33 * x[2]])

    def func1(x):
        return np.array([x[1]])

    def func2(x):
        return np.array([x[2]])

    cons = ({'type': 'ineq', 'fun': func},
            {'type': 'ineq', 'fun': func1},
            {'type': 'ineq', 'fun': func2})

    def f(x):
        return -1 * (x[0] + x[1] + x[2])

    res = optimize.minimize(f, [0, 0, 0], method='SLSQP', constraints=cons)
    assert_allclose(res.x, [125, 0, 0], atol=1e-10)

