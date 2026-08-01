
def test_block_lu_decomposition():
    A = MatrixSymbol('A', n, n)
    B = MatrixSymbol('B', n, m)
    C = MatrixSymbol('C', m, n)
    D = MatrixSymbol('D', m, m)
    X = BlockMatrix([[A, B], [C, D]])

    #LDU decomposition
    L, D, U = X.LDUdecomposition()
    assert block_collapse(L*D*U) == X

    #UDL decomposition
    U, D, L = X.UDLdecomposition()
    assert block_collapse(U*D*L) == X

    #LU decomposition
    L, U = X.LUdecomposition()
    assert block_collapse(L*U) == X

