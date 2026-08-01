
def test_trace_as_explicit():
    raises(ValueError, lambda: Trace(A).as_explicit())

    X = MatrixSymbol("X", 3, 3)
    assert Trace(X).as_explicit() == X[0, 0] + X[1, 1] + X[2, 2]
    assert Trace(eye(3)).as_explicit() == 3

