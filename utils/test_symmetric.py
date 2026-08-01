
def test_symmetric():
    assert ask(Q.symmetric(X), Q.symmetric(X))
    assert ask(Q.symmetric(X*Z), Q.symmetric(X)) is None
    assert ask(Q.symmetric(X*Z), Q.symmetric(X) & Q.symmetric(Z)) is True
    assert ask(Q.symmetric(X + Z), Q.symmetric(X) & Q.symmetric(Z)) is True
    assert ask(Q.symmetric(Y)) is False
    assert ask(Q.symmetric(Y*Y.T)) is True
    assert ask(Q.symmetric(Y.T*X*Y)) is None
    assert ask(Q.symmetric(Y.T*X*Y), Q.symmetric(X)) is True
    assert ask(Q.symmetric(X**10), Q.symmetric(X)) is True
    assert ask(Q.symmetric(A1x1)) is True
    assert ask(Q.symmetric(A1x1 + B1x1)) is True
    assert ask(Q.symmetric(A1x1 * B1x1)) is True
    assert ask(Q.symmetric(V1.T*V1)) is True
    assert ask(Q.symmetric(V1.T*(V1 + V2))) is True
    assert ask(Q.symmetric(V1.T*(V1 + V2) + A1x1)) is True
    assert ask(Q.symmetric(MatrixSlice(Y, (0, 1), (1, 2)))) is True
    assert ask(Q.symmetric(Identity(3))) is True
    assert ask(Q.symmetric(ZeroMatrix(3, 3))) is True
    assert ask(Q.symmetric(OneMatrix(3, 3))) is True


def test_symmetric(xp):

    for win in [windows.lanczos]:
        # Even sampling points
        w = win(4096, xp=xp)
        flip = array_namespace(w).flip
        error = xp.max(xp.abs(w - flip(w)))
        xp_assert_equal(error, xp.asarray(0.0), check_dtype=False, check_0d=False)

        # Odd sampling points
        w = win(4097, xp=xp)
        error = xp.max(xp.abs(w - flip(w)))
        xp_assert_equal(error, xp.asarray(0.0), check_dtype=False, check_0d=False)

