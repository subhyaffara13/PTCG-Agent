
def test_maple_matrix_assign_to_more():
    # assigning to Symbol or MatrixSymbol requires lhs/rhs match
    A = Matrix([[1, 2, 3]])
    B = MatrixSymbol('B', 1, 3)
    C = MatrixSymbol('C', 2, 3)
    assert maple_code(A, assign_to=B) == "B := Matrix([[1, 2, 3]], storage = rectangular)"
    raises(ValueError, lambda: maple_code(A, assign_to=x))
    raises(ValueError, lambda: maple_code(A, assign_to=C))

