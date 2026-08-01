
def test_QRsolve():
    A = Matrix([[2, 3, 5],
                [3, 6, 2],
                [8, 3, 6]])
    x = Matrix(3, 1, [3, 7, 5])
    b = A*x
    soln = A.QRsolve(b)
    assert soln == x
    x = Matrix([[1, 2], [3, 4], [5, 6]])
    b = A*x
    soln = A.QRsolve(b)
    assert soln == x

    A = Matrix([[0, -1, 2],
                [5, 10, 7],
                [8,  3, 4]])
    x = Matrix(3, 1, [-1, 2, 5])
    b = A*x
    soln = A.QRsolve(b)
    assert soln == x
    x = Matrix([[7, 8], [9, 10], [11, 12]])
    b = A*x
    soln = A.QRsolve(b)
    assert soln == x

