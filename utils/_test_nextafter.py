
def _test_nextafter(t):
    one = t(1)
    two = t(2)
    zero = t(0)
    eps = np.finfo(t).eps
    assert_(np.nextafter(one, two) - one == eps)
    assert_(np.nextafter(one, zero) - one < 0)
    assert_(np.isnan(np.nextafter(np.nan, one)))
    assert_(np.isnan(np.nextafter(one, np.nan)))
    assert_(np.nextafter(one, one) == one)

