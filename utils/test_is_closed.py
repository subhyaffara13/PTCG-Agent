
def test_is_closed():
    assert Interval(0, 1, False, False).is_closed is True
    assert Interval(0, 1, True, False).is_closed is False
    assert FiniteSet(1, 2, 3).is_closed is True

