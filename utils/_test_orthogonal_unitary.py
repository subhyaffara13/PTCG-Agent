
def _test_orthogonal_unitary(predicate):
    assert ask(predicate(X), predicate(X))
    assert ask(predicate(X.T), predicate(X)) is True
    assert ask(predicate(X.I), predicate(X)) is True
    assert ask(predicate(X**2), predicate(X))
    assert ask(predicate(Y)) is False
    assert ask(predicate(X)) is None
    assert ask(predicate(X), ~Q.invertible(X)) is False
    assert ask(predicate(X*Z*X), predicate(X) & predicate(Z)) is True
    assert ask(predicate(Identity(3))) is True
    assert ask(predicate(ZeroMatrix(3, 3))) is False
    assert ask(Q.invertible(X), predicate(X))
    assert not ask(predicate(X + Z), predicate(X) & predicate(Z))

