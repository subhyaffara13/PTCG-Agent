
def test_cse_matrix_negate_matrix():
    A = ImmutableDenseMatrix(symbols('A:4')).reshape(2, 2)
    x = MatMul(S.NegativeOne, A)
    cse_expr = cse(x)
    assert cse_expr == ([], [x])

