
def test_tbound_respected_small_interval(method):
    """Regression test for gh-17341"""
    SMALL = 1e-4

    # f[y(t)] = 2y(t) on t in [0,SMALL]
    #           undefined otherwise
    def f(t, y):
        if t > SMALL:
            raise ValueError("Function was evaluated outside interval")
        return 2 * y
    res = solve_ivp(f, (0.0, SMALL), np.array([1]), method=method)
    assert res.success

