
def test_MatMul_MatAdd():
    X, Y = MatrixSymbol("X", 2, 2), MatrixSymbol("Y", 2, 2)
    assert str(2*(X + Y)) == "2*X + 2*Y"

    assert str(I*X) == "I*X"
    assert str(-I*X) == "-I*X"
    assert str((1 + I)*X) == '(1 + I)*X'
    assert str(-(1 + I)*X) == '(-1 - I)*X'
    assert str(MatAdd(MatAdd(X, Y), MatAdd(X, Y))) == '(X + Y) + (X + Y)'

