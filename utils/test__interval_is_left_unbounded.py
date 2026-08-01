
def test_Interval_is_left_unbounded():
    assert Interval(3, 4).is_left_unbounded is False
    assert Interval(-oo, 3).is_left_unbounded is True
    assert Interval(Float("-inf"), 3).is_left_unbounded is True

