
def test_bogus_string():
    assert_raises(ValueError, np.longdouble, "spam")
    assert_raises(ValueError, np.longdouble, "1.0 flub")

