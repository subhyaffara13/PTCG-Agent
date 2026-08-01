
def test_cramer_solve_errors(det_method, error):
    # Non-square matrix
    A = Matrix([[0, -1, 2], [5, 10, 7]])
    b = Matrix([-2, 15])
    raises(error, lambda: A.cramer_solve(b, det_method=det_method))

