
def test_maple_matrix_assign_to():
    A = Matrix([[1, 2, 3]])
    assert maple_code(A, assign_to='a') == "a := Matrix([[1, 2, 3]], storage = rectangular)"
    A = Matrix([[1, 2], [3, 4]])
    assert maple_code(A, assign_to='A') == "A := Matrix([[1, 2], [3, 4]], storage = rectangular)"

