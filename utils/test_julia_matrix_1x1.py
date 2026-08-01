
def test_julia_matrix_1x1():
    A = Matrix([[3]])
    B = MatrixSymbol('B', 1, 1)
    C = MatrixSymbol('C', 1, 2)
    assert julia_code(A, assign_to=B) == "B = [3]"
    # FIXME?
    #assert julia_code(A, assign_to=x) == "x = [3]"
    raises(ValueError, lambda: julia_code(A, assign_to=C))

