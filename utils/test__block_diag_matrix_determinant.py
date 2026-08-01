
def test_BlockDiagMatrix_determinant():
    A = MatrixSymbol('A', n, n)
    B = MatrixSymbol('B', m, m)
    assert det(BlockDiagMatrix()) == 1
    assert det(BlockDiagMatrix(A)) == det(A)
    assert det(BlockDiagMatrix(A, B)) == det(A) * det(B)

    # non-square blocks
    C = MatrixSymbol('C', m, n)
    D = MatrixSymbol('D', n, m)
    assert det(BlockDiagMatrix(C, D)) == 0

