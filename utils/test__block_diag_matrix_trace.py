
def test_BlockDiagMatrix_trace():
    assert trace(BlockDiagMatrix()) == 0
    assert trace(BlockDiagMatrix(ZeroMatrix(n, n))) == 0
    A = MatrixSymbol('A', n, n)
    assert trace(BlockDiagMatrix(A)) == trace(A)
    B = MatrixSymbol('B', m, m)
    assert trace(BlockDiagMatrix(A, B)) == trace(A) + trace(B)

    # non-square blocks
    C = MatrixSymbol('C', m, n)
    D = MatrixSymbol('D', n, m)
    assert isinstance(trace(BlockDiagMatrix(C, D)), Trace)

