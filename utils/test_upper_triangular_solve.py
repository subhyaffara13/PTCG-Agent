
def test_upper_triangular_solve():

    raises(NonSquareMatrixError,
        lambda: Matrix([1, 0]).upper_triangular_solve(Matrix([0, 1])))
    raises(ShapeError,
        lambda: Matrix([[1, 0], [0, 1]]).upper_triangular_solve(Matrix([1])))
    raises(TypeError,
        lambda: Matrix([[2, 1], [1, 2]]).upper_triangular_solve(
            Matrix([[1, 0], [0, 1]])))

    A = Matrix([[1, 0], [0, 1]])
    B = Matrix([[x, y], [y, x]])
    C = Matrix([[2, 4], [3, 8]])

    assert A.upper_triangular_solve(B) == B
    assert A.upper_triangular_solve(C) == C


def test_upper_triangular_solve():
    raises(NonSquareMatrixError, lambda:
        SparseMatrix([[1, 2]]).upper_triangular_solve(Matrix([[1, 2]])))
    raises(ShapeError, lambda:
        SparseMatrix([[1, 2], [0, 4]]).upper_triangular_solve(Matrix([1])))
    raises(TypeError, lambda:
        SparseMatrix([[1, 2], [3, 4]]).upper_triangular_solve(Matrix([[1, 2], [3, 4]])))

    a, b, c, d = symbols('a:d')
    u, v, w, x = symbols('u:x')

    A = SparseMatrix([[a, b], [0, d]])
    B = MutableSparseMatrix([[u, v], [w, x]])
    C = ImmutableSparseMatrix([[u, v], [w, x]])

    sol = Matrix([[(u - b*w/d)/a, (v - b*x/d)/a], [w/d, x/d]])
    assert A.upper_triangular_solve(B) == sol
    assert A.upper_triangular_solve(C) == sol

