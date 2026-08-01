
def test_matrix_zeros_sympy():
    sym = matrix_zeros(4, 4, format='sympy')
    assert isinstance(sym, Matrix)

