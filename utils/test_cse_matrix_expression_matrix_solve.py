
def test_cse_matrix_expression_matrix_solve():
    A = ImmutableDenseMatrix(symbols('A:4')).reshape(2, 2)
    b = ImmutableDenseMatrix(symbols('b:2'))
    x = MatrixSolve(A, b)
    cse_expr = cse(x)
    assert cse_expr == ([], [x])

