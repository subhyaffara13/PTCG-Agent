
def test_hypotest_back_compat_no_axis(fun, nsamp):
    m, n = 8, 9

    rng = np.random.default_rng(0)
    x = rng.random((nsamp, m, n))
    res = fun(*x)
    res2 = fun(*x, _no_deco=True)
    res3 = fun([xi.ravel() for xi in x])
    assert_equal(res, res2)
    assert_equal(res, res3)

