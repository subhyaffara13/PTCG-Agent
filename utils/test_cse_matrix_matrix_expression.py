
def test_cse_matrix_matrix_expression():
    X = ImmutableDenseMatrix(symbols('X:4')).reshape(2, 2)
    y = ImmutableDenseMatrix(symbols('y:2'))
    b = MatMul(Inverse(MatMul(Transpose(X), X)), Transpose(X), y)
    cse_expr = cse(b)
    x0 = MatrixSymbol('x0', 2, 2)
    reduced_expr_expected = MatMul(Inverse(MatMul(x0, X)), x0, y)
    assert cse_expr == ([(x0, Transpose(X))], [reduced_expr_expected])

