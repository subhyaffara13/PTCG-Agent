
def test_issue_8777():
    assert And(x > 2, x < oo).as_set() == Interval(2, oo, left_open=True)
    assert And(x >= 1, x < oo).as_set() == Interval(1, oo)
    assert (x < oo).as_set() == Interval(-oo, oo)
    assert (x > -oo).as_set() == Interval(-oo, oo)

