
def test_matrix_solve_issue_24862():
    A = Matrix(3, 3, symbols('a:9'))
    b = Matrix(3, 1, symbols('b:3'))
    hash(MatrixSolve(A, b))

