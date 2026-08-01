
def test_dense_conversion():
    X = MatrixSymbol('X', 2, 2)
    assert ImmutableMatrix(X) == ImmutableMatrix(2, 2, lambda i, j: X[i, j])
    assert Matrix(X) == Matrix(2, 2, lambda i, j: X[i, j])

