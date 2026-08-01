
def test_P12():
    A11 = MatrixSymbol('A11', n, n)
    A12 = MatrixSymbol('A12', n, n)
    A22 = MatrixSymbol('A22', n, n)
    B = BlockMatrix([[A11, A12],
                     [ZeroMatrix(n, n), A22]])
    assert block_collapse(B.I) == BlockMatrix([[A11.I, (-1)*A11.I*A12*A22.I],
                                               [ZeroMatrix(n, n), A22.I]])

