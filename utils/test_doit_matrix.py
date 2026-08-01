
def test_doit_matrix():
    X = ImmutableMatrix([[1, 2], [3, 4]])
    assert MatPow(X, 0).doit() == ImmutableMatrix(Identity(2))
    assert MatPow(X, 1).doit() == X
    assert MatPow(X, 2).doit() == X**2
    assert MatPow(X, -1).doit() == X.inv()
    assert MatPow(X, -2).doit() == (X.inv())**2
    # less expensive than testing on a 2x2
    assert MatPow(ImmutableMatrix([4]), S.Half).doit() == ImmutableMatrix([2])
    X = ImmutableMatrix([[0, 2], [0, 4]]) # det() == 0
    raises(ValueError, lambda: MatPow(X,-1).doit())
    raises(ValueError, lambda: MatPow(X,-2).doit())

