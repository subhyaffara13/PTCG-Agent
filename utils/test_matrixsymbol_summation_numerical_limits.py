
def test_matrixsymbol_summation_numerical_limits():
    A = MatrixSymbol('A', 3, 3)
    n = Symbol('n', integer=True)

    assert Sum(A**n, (n, 0, 2)).doit() == Identity(3) + A + A**2
    assert Sum(A, (n, 0, 2)).doit() == 3*A
    assert Sum(n*A, (n, 0, 2)).doit() == 3*A

    B = Matrix([[0, n, 0], [-1, 0, 0], [0, 0, 2]])
    ans = Matrix([[0, 6, 0], [-4, 0, 0], [0, 0, 8]]) + 4*A
    assert Sum(A+B, (n, 0, 3)).doit() == ans
    ans = A*Matrix([[0, 6, 0], [-4, 0, 0], [0, 0, 8]])
    assert Sum(A*B, (n, 0, 3)).doit() == ans

    ans = (A**2*Matrix([[-2, 0, 0], [0,-2, 0], [0, 0, 4]]) +
           A**3*Matrix([[0, -9, 0], [3, 0, 0], [0, 0, 8]]) +
           A*Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 2]]))
    assert Sum(A**n*B**n, (n, 1, 3)).doit() == ans

