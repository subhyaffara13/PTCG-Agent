
def test_cse_matrix_optimize_out_single_argument_add_combined():
    A = ImmutableDenseMatrix(symbols('A:4')).reshape(2, 2)
    x = MatMul(MatAdd(MatAdd(MatAdd(A))), MatAdd(MatAdd(A)), MatAdd(A), A)
    cse_expr = cse(x)
    assert cse_expr == ([], [MatMul(4, A)])

