
def test_is_decreasing():
    """Test whether is_decreasing returns correct value."""
    b = Symbol('b', positive=True)

    assert is_decreasing(1/(x**2 - 3*x), Interval.open(Rational(3,2), 3))
    assert is_decreasing(1/(x**2 - 3*x), Interval.open(1.5, 3))
    assert is_decreasing(1/(x**2 - 3*x), Interval.Lopen(3, oo))
    assert not is_decreasing(1/(x**2 - 3*x), Interval.Ropen(-oo, Rational(3, 2)))
    assert not is_decreasing(-x**2, Interval(-oo, 0))
    assert not is_decreasing(-x**2*b, Interval(-oo, 0), x)

