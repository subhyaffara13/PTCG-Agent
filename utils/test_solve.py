
def test_solve():
    A = Matrix([[1,2], [2,4]])
    b = Matrix([[3], [4]])
    raises(ValueError, lambda: A.solve(b)) #no solution
    b = Matrix([[ 4], [8]])
    raises(ValueError, lambda: A.solve(b)) #infinite solution


def test_solve():
    assert norm(residual(A6, lu_solve(A6, b6), b6), inf) < 1.e-10
    assert norm(residual(A7, lu_solve(A7, b7), b7), inf) < 1.5
    assert norm(residual(A8, lu_solve(A8, b8), b8), inf) <= 3 + 1.e-10
    assert norm(residual(A6, qr_solve(A6, b6)[0], b6), inf) < 1.e-10
    assert norm(residual(A7, qr_solve(A7, b7)[0], b7), inf) < 1.5
    assert norm(residual(A8, qr_solve(A8, b8)[0], b8), 2) <= 4.3
    assert norm(residual(A10, lu_solve(A10, b10), b10), 2) < 1.e-10
    assert norm(residual(A10, qr_solve(A10, b10)[0], b10), 2) < 1.e-10

