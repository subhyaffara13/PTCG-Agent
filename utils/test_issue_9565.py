
def test_issue_9565():
    assert solveset_real(Abs((x - 1)/(x - 5)) <= Rational(1, 3), x) == Interval(-1, 2)

