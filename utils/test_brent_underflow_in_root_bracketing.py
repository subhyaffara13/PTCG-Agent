
def test_brent_underflow_in_root_bracketing():
    # Testing if an interval [a,b] brackets a zero of a function
    # by checking f(a)*f(b) < 0 is not reliable when the product
    # underflows/overflows. (reported in issue# 13737)

    underflow_scenario = (-450.0, -350.0, -400.0)
    overflow_scenario = (350.0, 450.0, 400.0)

    for a, b, root in [underflow_scenario, overflow_scenario]:
        c = np.exp(root)
        for method in [zeros.brenth, zeros.brentq]:
            res = method(lambda x: np.exp(x)-c, a, b)
            assert_allclose(root, res)

