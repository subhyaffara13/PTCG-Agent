
def test_julia_matrix_assign_to():
    A = Matrix([[1, 2, 3]])
    assert julia_code(A, assign_to='a') == "a = [1 2 3]"
    A = Matrix([[1, 2], [3, 4]])
    assert julia_code(A, assign_to='A') == "A = [1 2;\n3 4]"

