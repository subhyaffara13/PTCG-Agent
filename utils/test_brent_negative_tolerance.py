
def test_brent_negative_tolerance():
    assert_raises(ValueError, optimize.brent, np.cos, tol=-.01)

