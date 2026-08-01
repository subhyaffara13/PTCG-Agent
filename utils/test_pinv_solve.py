
def test_pinv_solve():
    # Fully determined system (unique result, identical to other solvers).
    A = Matrix([[1, 5], [7, 9]])
    B = Matrix([12, 13])
    assert A.pinv_solve(B) == A.cholesky_solve(B)
    assert A.pinv_solve(B) == A.LDLsolve(B)
    assert A.pinv_solve(B) == Matrix([sympify('-43/26'), sympify('71/26')])
    assert A * A.pinv() * B == B
    # Fully determined, with two-dimensional B matrix.
    B = Matrix([[12, 13, 14], [15, 16, 17]])
    assert A.pinv_solve(B) == A.cholesky_solve(B)
    assert A.pinv_solve(B) == A.LDLsolve(B)
    assert A.pinv_solve(B) == Matrix([[-33, -37, -41], [69, 75, 81]]) / 26
    assert A * A.pinv() * B == B
    # Underdetermined system (infinite results).
    A = Matrix([[1, 0, 1], [0, 1, 1]])
    B = Matrix([5, 7])
    solution = A.pinv_solve(B)
    w = {}
    for s in solution.atoms(Symbol):
        # Extract dummy symbols used in the solution.
        w[s.name] = s
    assert solution == Matrix([[w['w0_0']/3 + w['w1_0']/3 - w['w2_0']/3 + 1],
                               [w['w0_0']/3 + w['w1_0']/3 - w['w2_0']/3 + 3],
                               [-w['w0_0']/3 - w['w1_0']/3 + w['w2_0']/3 + 4]])
    assert A * A.pinv() * B == B
    # Overdetermined system (least squares results).
    A = Matrix([[1, 0], [0, 0], [0, 1]])
    B = Matrix([3, 2, 1])
    assert A.pinv_solve(B) == Matrix([3, 1])
    # Proof the solution is not exact.
    assert A * A.pinv() * B != B

