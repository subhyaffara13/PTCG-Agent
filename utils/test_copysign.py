
def test_copysign():
    assert_(np.copysign(1, -1) == -1)
    with np.errstate(divide="ignore"):
        assert_(1 / np.copysign(0, -1) < 0)
        assert_(1 / np.copysign(0, 1) > 0)
    assert_(np.signbit(np.copysign(np.nan, -1)))
    assert_(not np.signbit(np.copysign(np.nan, 1)))

