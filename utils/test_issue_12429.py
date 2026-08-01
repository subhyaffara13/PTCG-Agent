
def test_issue_12429():
    eq = solveset(log(x)/x <= 0, x, S.Reals)
    sol = Interval.Lopen(0, 1)
    assert eq == sol

