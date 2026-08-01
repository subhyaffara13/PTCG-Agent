
def test_invertible():
    assert ask(Q.invertible(X), Q.invertible(X))
    assert ask(Q.invertible(Y)) is False
    assert ask(Q.invertible(X*Y), Q.invertible(X)) is False
    assert ask(Q.invertible(X*Z), Q.invertible(X)) is None
    assert ask(Q.invertible(X*Z), Q.invertible(X) & Q.invertible(Z)) is True
    assert ask(Q.invertible(X.T)) is None
    assert ask(Q.invertible(X.T), Q.invertible(X)) is True
    assert ask(Q.invertible(X.I)) is True
    assert ask(Q.invertible(Identity(3))) is True
    assert ask(Q.invertible(ZeroMatrix(3, 3))) is False
    assert ask(Q.invertible(OneMatrix(1, 1))) is True
    assert ask(Q.invertible(OneMatrix(3, 3))) is False
    assert ask(Q.invertible(X), Q.fullrank(X) & Q.square(X))


def test_invertible():
    A = MatrixSymbol('A', 5, 5)
    B = MatrixSymbol('B', 5, 5)
    assert satask(Q.invertible(A*B), Q.invertible(A) & Q.invertible(B)) is True
    assert satask(Q.invertible(A), Q.invertible(A*B)) is True
    assert satask(Q.invertible(A) & Q.invertible(B), Q.invertible(A*B)) is True


def test_invertible():
    """Verify `invertible` property. """
    SFT = ShortTimeFFT(np.ones(8), hop=4, fs=1)
    assert SFT.invertible
    SFT = ShortTimeFFT(np.ones(8), hop=9, fs=1)
    assert not SFT.invertible

