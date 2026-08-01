
def test_BlockDiagMatrix_transpose():
    A = MatrixSymbol('A', n, m)
    B = MatrixSymbol('B', k, l)
    assert transpose(BlockDiagMatrix()) == BlockDiagMatrix()
    assert transpose(BlockDiagMatrix(A)) == BlockDiagMatrix(A.T)
    assert transpose(BlockDiagMatrix(A, B)) == BlockDiagMatrix(A.T, B.T)

