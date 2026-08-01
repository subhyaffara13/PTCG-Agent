
def test_issue_13324():
    X = Uniform('X', 0, 1)
    assert E(X, X > S.Half) == Rational(3, 4)
    assert E(X, X > 0) == S.Half

