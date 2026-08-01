
def test_cse_matrix_expression_inverse():
    A = ImmutableDenseMatrix(symbols('A:4')).reshape(2, 2)
    x = Inverse(A)
    cse_expr = cse(x)
    assert cse_expr == ([], [Inverse(A)])

