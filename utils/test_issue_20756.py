
def test_issue_20756():
    X = Uniform('X', -1, +1)
    Y = Uniform('Y', -1, +1)
    assert E(X * Y) == S.Zero
    assert E(X * ((Y + 1) - 1)) == S.Zero
    assert E(Y * (X*(X + 1) - X*X)) == S.Zero

