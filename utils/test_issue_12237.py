
def test_issue_12237():
    X = Normal('X', 0, 1)
    Y = Normal('Y', 0, 1)
    U = P(X > 0, X)
    V = P(Y < 0, X)
    W = P(X + Y > 0, X)
    assert W == P(X + Y > 0, X)
    assert U == BernoulliDistribution(S.Half, S.Zero, S.One)
    assert V == S.Half

