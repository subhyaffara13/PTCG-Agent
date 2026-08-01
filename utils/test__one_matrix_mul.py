
def test_OneMatrix_mul():
    n, m, k = symbols('n m k', integer=True)
    w = MatrixSymbol('w', n, 1)
    assert OneMatrix(n, m) * OneMatrix(m, k) == OneMatrix(n, k) * m
    assert w * OneMatrix(1, 1) == w
    assert OneMatrix(1, 1) * w.T == w.T

