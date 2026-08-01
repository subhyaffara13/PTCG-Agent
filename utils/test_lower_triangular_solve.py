
def test_lower_triangular_solve():

    raises(NonSquareMatrixError,
        lambda: Matrix([1, 0]).lower_triangular_solve(Matrix([0, 1])))
    raises(ShapeError,
        lambda: Matrix([[1, 0], [0, 1]]).lower_triangular_solve(Matrix([1])))
    raises(ValueError,
        lambda: Matrix([[2, 1], [1, 2]]).lower_triangular_solve(
            Matrix([[1, 0], [0, 1]])))

    A = Matrix([[1, 0], [0, 1]])
    B = Matrix([[x, y], [y, x]])
    C = Matrix([[4, 8], [2, 9]])

    assert A.lower_triangular_solve(B) == B
    assert A.lower_triangular_solve(C) == C


def test_lower_triangular_solve():
    raises(NonSquareMatrixError, lambda:
        SparseMatrix([[1, 2]]).lower_triangular_solve(Matrix([[1, 2]])))
    raises(ShapeError, lambda:
        SparseMatrix([[1, 2], [0, 4]]).lower_triangular_solve(Matrix([1])))
    raises(ValueError, lambda:
        SparseMatrix([[1, 2], [3, 4]]).lower_triangular_solve(Matrix([[1, 2], [3, 4]])))

    a, b, c, d = symbols('a:d')
    u, v, w, x = symbols('u:x')

    A = SparseMatrix([[a, 0], [c, d]])
    B = MutableSparseMatrix([[u, v], [w, x]])
    C = ImmutableSparseMatrix([[u, v], [w, x]])

    sol = Matrix([[u/a, v/a], [(w - c*u/a)/d, (x - c*v/a)/d]])
    assert A.lower_triangular_solve(B) == sol
    assert A.lower_triangular_solve(C) == sol

