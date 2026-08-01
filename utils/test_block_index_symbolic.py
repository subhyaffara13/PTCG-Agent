
def test_block_index_symbolic():
    # Note that these matrices may be zero-sized and indices may be negative, which causes
    # all naive simplifications given in the comments to be invalid
    A1 = MatrixSymbol('A1', n, k)
    A2 = MatrixSymbol('A2', n, l)
    A3 = MatrixSymbol('A3', m, k)
    A4 = MatrixSymbol('A4', m, l)
    A = BlockMatrix([[A1, A2], [A3, A4]])
    assert A[0, 0] == MatrixElement(A, 0, 0)  # Cannot be A1[0, 0]
    assert A[n - 1, k - 1] == A1[n - 1, k - 1]
    assert A[n, k] == A4[0, 0]
    assert A[n + m - 1, 0] == MatrixElement(A, n + m - 1, 0)  # Cannot be A3[m - 1, 0]
    assert A[0, k + l - 1] == MatrixElement(A, 0, k + l - 1)  # Cannot be A2[0, l - 1]
    assert A[n + m - 1, k + l - 1] == MatrixElement(A, n + m - 1, k + l - 1)  # Cannot be A4[m - 1, l - 1]
    assert A[i, j] == MatrixElement(A, i, j)
    assert A[n + i, k + j] == MatrixElement(A, n + i, k + j)  # Cannot be A4[i, j]
    assert A[n - i - 1, k - j - 1] == MatrixElement(A, n - i - 1, k - j - 1)  # Cannot be A1[n - i - 1, k - j - 1]

