
def test_Integer_new():
    """
    Test for Integer constructor
    """
    _test_rational_new(Integer)

    assert _strictly_equal(Integer(0.9), S.Zero)
    assert _strictly_equal(Integer(10.5), Integer(10))
    raises(ValueError, lambda: Integer("10.5"))
    assert Integer(Rational('1.' + '9'*20)) == 1

