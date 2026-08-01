
def _test_rational_new(cls):
    """
    Tests that are common between Integer and Rational.
    """
    assert cls(0) is S.Zero
    assert cls(1) is S.One
    assert cls(-1) is S.NegativeOne
    # These look odd, but are similar to int():
    assert cls('1') is S.One
    assert cls('-1') is S.NegativeOne

    i = Integer(10)
    assert _strictly_equal(i, cls('10'))
    assert _strictly_equal(i, cls('10'))
    assert _strictly_equal(i, cls(int(10)))
    assert _strictly_equal(i, cls(i))

    raises(TypeError, lambda: cls(Symbol('x')))

