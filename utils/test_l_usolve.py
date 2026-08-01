
def test_LUsolve():
    A = Matrix([[2, 3, 5],
                [3, 6, 2],
                [8, 3, 6]])
    x = Matrix(3, 1, [3, 7, 5])
    b = A*x
    soln = A.LUsolve(b)
    assert soln == x
    A = Matrix([[0, -1, 2],
                [5, 10, 7],
                [8,  3, 4]])
    x = Matrix(3, 1, [-1, 2, 5])
    b = A*x
    soln = A.LUsolve(b)
    assert soln == x
    A = Matrix([[2, 1], [1, 0], [1, 0]])   # issue 14548
    b = Matrix([3, 1, 1])
    assert A.LUsolve(b) == Matrix([1, 1])
    b = Matrix([3, 1, 2])                  # inconsistent
    raises(ValueError, lambda: A.LUsolve(b))
    A = Matrix([[0, -1, 2],
                [5, 10, 7],
                [8,  3, 4],
                [2, 3, 5],
                [3, 6, 2],
                [8, 3, 6]])
    x = Matrix([2, 1, -4])
    b = A*x
    soln = A.LUsolve(b)
    assert soln == x
    A = Matrix([[0, -1, 2], [5, 10, 7]])  # underdetermined
    x = Matrix([-1, 2, 0])
    b = A*x
    raises(NotImplementedError, lambda: A.LUsolve(b))

    A = Matrix(4, 4, lambda i, j: 1/(i+j+1) if i != 3 else 0)
    b = Matrix.zeros(4, 1)
    raises(NonInvertibleMatrixError, lambda: A.LUsolve(b))

