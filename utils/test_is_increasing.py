
def test_is_increasing():
    """Test whether is_increasing returns correct value."""
    a = Symbol('a', negative=True)

    assert is_increasing(x**3 - 3*x**2 + 4*x, S.Reals)
    assert is_increasing(-x**2, Interval(-oo, 0))
    assert not is_increasing(-x**2, Interval(0, oo))
    assert not is_increasing(4*x**3 - 6*x**2 - 72*x + 30, Interval(-2, 3))
    assert is_increasing(x**2 + y, Interval(1, oo), x)
    assert is_increasing(-x**2*a, Interval(1, oo), x)
    assert is_increasing(1)

    assert is_increasing(4*x**3 - 6*x**2 - 72*x + 30, Interval(-2, 3)) is False

