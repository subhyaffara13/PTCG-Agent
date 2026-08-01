
def test_issue_10069():
    eq = abs(1/(x - 1)) - 1 > 0
    assert solveset_real(eq, x) == Union(
        Interval.open(0, 1), Interval.open(1, 2))

