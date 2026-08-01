
def test_issue_9324():
    def count(val):
        return count_ops(val, visual=False)

    M = MatrixSymbol('M', 10, 10)
    assert count(M[0, 0]) == 0
    assert count(2 * M[0, 0] + M[5, 7]) == 2
    P = MatrixSymbol('P', 3, 3)
    Q = MatrixSymbol('Q', 3, 3)
    assert count(P + Q) == 1
    m = Symbol('m', integer=True)
    n = Symbol('n', integer=True)
    M = MatrixSymbol('M', m + n, m * m)
    assert count(M[0, 1]) == 2

