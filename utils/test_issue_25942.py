
def test_issue_25942():
    assert (acos(x) > pi/3).as_set() == Interval.Ropen(-1, S(1)/2)

