
def test_non_trivial_implies():
    X = MatrixSymbol('X', 3, 3)
    Y = MatrixSymbol('Y', 3, 3)
    assert ask(Q.lower_triangular(X+Y), Q.lower_triangular(X) &
               Q.lower_triangular(Y)) is True
    assert ask(Q.triangular(X), Q.lower_triangular(X)) is True
    assert ask(Q.triangular(X+Y), Q.lower_triangular(X) &
               Q.lower_triangular(Y)) is True

