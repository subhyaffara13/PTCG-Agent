
def test_issue_10052():
    X = Exponential('X', 3)
    assert P(X < oo) == 1
    assert P(X > oo) == 0
    assert P(X < 2, X > oo) == 0
    assert P(X < oo, X > oo) == 0
    assert P(X < oo, X > 2) == 1
    assert P(X < 3, X == 2) == 0
    raises(ValueError, lambda: P(1))
    raises(ValueError, lambda: P(X < 1, 2))

