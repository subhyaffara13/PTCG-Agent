
def test_positive_definite():
    assert ask(Q.positive_definite(X), Q.positive_definite(X))
    assert ask(Q.positive_definite(X.T), Q.positive_definite(X)) is True
    assert ask(Q.positive_definite(X.I), Q.positive_definite(X)) is True
    assert ask(Q.positive_definite(Y)) is False
    assert ask(Q.positive_definite(X)) is None
    assert ask(Q.positive_definite(X**3), Q.positive_definite(X))
    assert ask(Q.positive_definite(X*Z*X),
            Q.positive_definite(X) & Q.positive_definite(Z)) is True
    assert ask(Q.positive_definite(X), Q.orthogonal(X))
    assert ask(Q.positive_definite(Y.T*X*Y),
            Q.positive_definite(X) & Q.fullrank(Y)) is True
    assert not ask(Q.positive_definite(Y.T*X*Y), Q.positive_definite(X))
    assert ask(Q.positive_definite(Identity(3))) is True
    assert ask(Q.positive_definite(ZeroMatrix(3, 3))) is False
    assert ask(Q.positive_definite(OneMatrix(1, 1))) is True
    assert ask(Q.positive_definite(OneMatrix(3, 3))) is False
    assert ask(Q.positive_definite(X + Z), Q.positive_definite(X) &
            Q.positive_definite(Z)) is True
    assert not ask(Q.positive_definite(-X), Q.positive_definite(X))
    assert ask(Q.positive(X[1, 1]), Q.positive_definite(X))

