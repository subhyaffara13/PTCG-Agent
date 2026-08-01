
def test_octave_matrix_assign_to_more():
    # assigning to Symbol or MatrixSymbol requires lhs/rhs match
    A = Matrix([[1, 2, 3]])
    B = MatrixSymbol('B', 1, 3)
    C = MatrixSymbol('C', 2, 3)
    assert mcode(A, assign_to=B) == "B = [1 2 3];"
    raises(ValueError, lambda: mcode(A, assign_to=x))
    raises(ValueError, lambda: mcode(A, assign_to=C))

