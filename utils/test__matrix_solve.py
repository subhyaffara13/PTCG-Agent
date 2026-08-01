
def test_MatrixSolve():
    n = Symbol('n', integer=True)
    A = MatrixSymbol('A', n, n)
    x = MatrixSymbol('x', n, 1)
    assert mcode(MatrixSolve(A, x)) == "A \\ x"

