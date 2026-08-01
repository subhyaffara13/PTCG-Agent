
def test_matrix_to_zero():
    assert matrix_to_zero(m) == m
    assert matrix_to_zero(Matrix([[0, 0], [0, 0]])) == Integer(0)

