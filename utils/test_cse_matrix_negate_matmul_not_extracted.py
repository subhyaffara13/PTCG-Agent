
def test_cse_matrix_negate_matmul_not_extracted():
    A = ImmutableDenseMatrix(symbols('A:4')).reshape(2, 2)
    B = ImmutableDenseMatrix(symbols('B:4')).reshape(2, 2)
    x = MatMul(S.NegativeOne, A, B)
    cse_expr = cse(x)
    assert cse_expr == ([], [x])

