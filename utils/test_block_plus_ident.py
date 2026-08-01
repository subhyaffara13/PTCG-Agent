
def test_block_plus_ident():
    A = MatrixSymbol('A', n, n)
    B = MatrixSymbol('B', n, m)
    C = MatrixSymbol('C', m, n)
    D = MatrixSymbol('D', m, m)
    X = BlockMatrix([[A, B], [C, D]])
    Z = MatrixSymbol('Z', n + m, n + m)
    assert bc_block_plus_ident(X + Identity(m + n) + Z) == \
            BlockDiagMatrix(Identity(n), Identity(m)) + X + Z

