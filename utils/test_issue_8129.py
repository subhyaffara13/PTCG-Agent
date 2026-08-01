
def test_issue_8129():
    X = Exponential('X', 4)
    assert P(X >= X) == 1
    assert P(X > X) == 0
    assert P(X > X+1) == 0

