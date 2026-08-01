
def test_block_index_large():
    n, m, k = symbols('n m k', integer=True, positive=True)
    i = symbols('i', integer=True, nonnegative=True)
    A1 = MatrixSymbol('A1', n, n)
    A2 = MatrixSymbol('A2', n, m)
    A3 = MatrixSymbol('A3', n, k)
    A4 = MatrixSymbol('A4', m, n)
    A5 = MatrixSymbol('A5', m, m)
    A6 = MatrixSymbol('A6', m, k)
    A7 = MatrixSymbol('A7', k, n)
    A8 = MatrixSymbol('A8', k, m)
    A9 = MatrixSymbol('A9', k, k)
    A = BlockMatrix([[A1, A2, A3], [A4, A5, A6], [A7, A8, A9]])
    assert A[n + i, n + i] == MatrixElement(A, n + i, n + i)

