
def test_is_strictly_increasing():
    """Test whether is_strictly_increasing returns correct value."""
    assert is_strictly_increasing(
        4*x**3 - 6*x**2 - 72*x + 30, Interval.Ropen(-oo, -2))
    assert is_strictly_increasing(
        4*x**3 - 6*x**2 - 72*x + 30, Interval.Lopen(3, oo))
    assert not is_strictly_increasing(
        4*x**3 - 6*x**2 - 72*x + 30, Interval.open(-2, 3))
    assert not is_strictly_increasing(-x**2, Interval(0, oo))
    assert not is_strictly_decreasing(1)

    assert is_strictly_increasing(4*x**3 - 6*x**2 - 72*x + 30, Interval.open(-2, 3)) is False

