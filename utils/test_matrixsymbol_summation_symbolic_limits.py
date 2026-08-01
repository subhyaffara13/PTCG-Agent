
def test_matrixsymbol_summation_symbolic_limits():
    N = Symbol('N', integer=True, positive=True)

    A = MatrixSymbol('A', 3, 3)
    n = Symbol('n', integer=True)
    assert Sum(A, (n, 0, N)).doit() == (N+1)*A
    assert Sum(n*A, (n, 0, N)).doit() == (N**2/2+N/2)*A

