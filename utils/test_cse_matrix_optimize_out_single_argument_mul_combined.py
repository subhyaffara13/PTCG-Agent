
def test_cse_matrix_optimize_out_single_argument_mul_combined():
    A = ImmutableDenseMatrix(symbols('A:4')).reshape(2, 2)
    x = MatAdd(MatMul(MatMul(MatMul(A))), MatMul(MatMul(A)), MatMul(A), A)
    cse_expr = cse(x)
    assert cse_expr == ([], [MatMul(4, A)])

