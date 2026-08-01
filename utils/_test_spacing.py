
def _test_spacing(t):
    one = t(1)
    eps = np.finfo(t).eps
    nan = t(np.nan)
    inf = t(np.inf)
    with np.errstate(invalid='ignore'):
        assert_equal(np.spacing(one), eps)
        assert_(np.isnan(np.spacing(nan)))
        assert_(np.isnan(np.spacing(inf)))
        assert_(np.isnan(np.spacing(-inf)))
        assert_(np.spacing(t(1e30)) != 0)

