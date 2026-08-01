
def test_matrix_solve_derivative_exact():
    q = symbols('q')
    a11, a12, a21, a22, b1, b2 = (
        f(q) for f in symbols('a11 a12 a21 a22 b1 b2', cls=Function))
    A = Matrix([[a11, a12], [a21, a22]])
    b = Matrix([b1, b2])
    x_lu = A.LUsolve(b)
    dxdq_lu = A.LUsolve(b.diff(q) - A.diff(q) * A.LUsolve(b))
    assert simplify(x_lu.diff(q) - dxdq_lu) == zeros(2, 1)
    # dxdq_ms is the MatrixSolve equivalent of dxdq_lu
    dxdq_ms = MatrixSolve(A, b.diff(q) - A.diff(q) * MatrixSolve(A, b))
    assert MatrixSolve(A, b).diff(q) == dxdq_ms

