
def test_issue_6810():
    X = Die('X', 6)
    Y = Normal('Y', 0, 1)
    assert P(Eq(X, 2)) == S(1)/6
    assert P(Eq(Y, 0)) == 0
    assert P(Or(X > 2, X < 3)) == 1
    assert P(And(X > 3, X > 2)) == S(1)/2

