
def test_LDLsolve():
    A = Matrix([[2, 3, 5],
                [3, 6, 2],
                [8, 3, 6]])
    x = Matrix(3, 1, [3, 7, 5])
    b = A*x
    soln = A.LDLsolve(b)
    assert soln == x

    A = Matrix([[0, -1, 2],
                [5, 10, 7],
                [8,  3, 4]])
    x = Matrix(3, 1, [-1, 2, 5])
    b = A*x
    soln = A.LDLsolve(b)
    assert soln == x

    A = Matrix(((9, 3*I), (-3*I, 5)))
    x = Matrix((-2, 1))
    b = A*x
    soln = A.LDLsolve(b)
    assert expand_mul(soln) == x

    A = Matrix(((9*I, 3), (-3 + I, 5)))
    x = Matrix((2 + 3*I, -1))
    b = A*x
    soln = A.LDLsolve(b)
    assert expand_mul(soln) == x

    A = Matrix(((9, 3), (3, 9)))
    x = Matrix((1, 1))
    b = A * x
    soln = A.LDLsolve(b)
    assert expand_mul(soln) == x

    A = Matrix([[-5, -3, -4], [-3, -7, 7]])
    x = Matrix([[8], [7], [-2]])
    b = A * x
    raises(NotImplementedError, lambda: A.LDLsolve(b))

