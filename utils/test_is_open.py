
def test_is_open():
    assert Interval(0, 1, False, False).is_open is False
    assert Interval(0, 1, True, False).is_open is False
    assert Interval(0, 1, True, True).is_open is True
    assert FiniteSet(1, 2, 3).is_open is False

