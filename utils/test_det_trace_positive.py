
def test_det_trace_positive():
    X = MatrixSymbol('X', 4, 4)
    assert ask(Q.positive(Trace(X)), Q.positive_definite(X))
    assert ask(Q.positive(Determinant(X)), Q.positive_definite(X))

