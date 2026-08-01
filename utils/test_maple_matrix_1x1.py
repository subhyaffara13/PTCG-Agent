
def test_maple_matrix_1x1():
    A = Matrix([[3]])
    assert maple_code(A, assign_to='B') == "B := Matrix([[3]], storage = rectangular)"

