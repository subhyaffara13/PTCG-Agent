
def test_Interval_is_right_unbounded():
    assert Interval(3, 4).is_right_unbounded is False
    assert Interval(3, oo).is_right_unbounded is True
    assert Interval(3, Float("+inf")).is_right_unbounded is True

