
def test_cse_matrix_optimize_out_single_argument_mul():
    A = ImmutableDenseMatrix(symbols('A:4')).reshape(2, 2)
    x = MatMul(MatMul(MatMul(A)))
    cse_expr = cse(x)
    assert cse_expr == ([], [A])

