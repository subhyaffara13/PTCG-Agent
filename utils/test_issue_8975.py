
def test_issue_8975():
    assert Or(And(-oo < x, x <= -2), And(2 <= x, x < oo)).as_set() == \
           Interval(-oo, -2) + Interval(2, oo)

