
def test_issue_24859():
    A = MatrixSymbol('A', 2, 3)
    B = MatrixSymbol('B', 3, 2)
    J = A*B
    Jinv = Matrix(J).adjugate()
    u = MatrixSymbol('u', 2, 3)
    Jk = Jinv.subs(A, A + x*u)

    expected = B[0, 1]*u[1, 0] + B[1, 1]*u[1, 1] + B[2, 1]*u[1, 2]
    assert Jk[0, 0].diff(x) == expected
    assert diff(Jk[0, 0], x).doit() == expected

