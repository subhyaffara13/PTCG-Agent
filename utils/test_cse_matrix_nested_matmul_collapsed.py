
def test_cse_matrix_nested_matmul_collapsed():
    A = ImmutableDenseMatrix(symbols('A:4')).reshape(2, 2)
    B = ImmutableDenseMatrix(symbols('B:4')).reshape(2, 2)
    x = MatMul(S.NegativeOne, MatMul(A, B))
    cse_expr = cse(x)
    assert cse_expr == ([], [MatMul(S.NegativeOne, A, B)])

