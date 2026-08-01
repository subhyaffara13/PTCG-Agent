
def test_diagonal_solve():
    raises(TypeError, lambda: Matrix([1, 1]).diagonal_solve(Matrix([1])))
    A = Matrix([[1, 0], [0, 1]])*2
    B = Matrix([[x, y], [y, x]])
    assert A.diagonal_solve(B) == B/2

    A = Matrix([[1, 0], [1, 2]])
    raises(TypeError, lambda: A.diagonal_solve(B))


def test_diagonal_solve():
    a, d = symbols('a d')
    u, v, w, x = symbols('u:x')

    A = SparseMatrix([[a, 0], [0, d]])
    B = MutableSparseMatrix([[u, v], [w, x]])
    C = ImmutableSparseMatrix([[u, v], [w, x]])

    sol = Matrix([[u/a, v/a], [w/d, x/d]])
    assert A.diagonal_solve(B) == sol
    assert A.diagonal_solve(C) == sol

