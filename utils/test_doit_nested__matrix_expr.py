
def test_doit_nested_MatrixExpr():
    X = ImmutableMatrix([[1, 2], [3, 4]])
    Y = ImmutableMatrix([[2, 3], [4, 5]])
    assert MatPow(MatMul(X, Y), 2).doit() == (X*Y)**2
    assert MatPow(MatAdd(X, Y), 2).doit() == (X + Y)**2

