
def test_bc_dist_diag():
    A = MatrixSymbol('A', n, n)
    B = MatrixSymbol('B', m, m)
    C = MatrixSymbol('C', l, l)
    X = BlockDiagMatrix(A, B, C)

    assert bc_dist(X+X).equals(BlockDiagMatrix(2*A, 2*B, 2*C))

