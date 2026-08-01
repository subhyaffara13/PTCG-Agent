
def test_BlockDiagMatrix():
    A = MatrixSymbol('A', n, n)
    B = MatrixSymbol('B', m, m)
    C = MatrixSymbol('C', l, l)
    M = MatrixSymbol('M', n + m + l, n + m + l)

    X = BlockDiagMatrix(A, B, C)
    Y = BlockDiagMatrix(A, 2*B, 3*C)

    assert X.blocks[1, 1] == B
    assert X.shape == (n + m + l, n + m + l)
    assert all(X.blocks[i, j].is_ZeroMatrix if i != j else X.blocks[i, j] in [A, B, C]
            for i in range(3) for j in range(3))
    assert X.__class__(*X.args) == X
    assert X.get_diag_blocks() == (A, B, C)

    assert isinstance(block_collapse(X.I * X), Identity)

    assert bc_matmul(X*X) == BlockDiagMatrix(A*A, B*B, C*C)
    assert block_collapse(X*X) == BlockDiagMatrix(A*A, B*B, C*C)
    #XXX: should be == ??
    assert block_collapse(X + X).equals(BlockDiagMatrix(2*A, 2*B, 2*C))
    assert block_collapse(X*Y) == BlockDiagMatrix(A*A, 2*B*B, 3*C*C)
    assert block_collapse(X + Y) == BlockDiagMatrix(2*A, 3*B, 4*C)

    # Ensure that BlockDiagMatrices can still interact with normal MatrixExprs
    assert (X*(2*M)).is_MatMul
    assert (X + (2*M)).is_MatAdd

    assert (X._blockmul(M)).is_MatMul
    assert (X._blockadd(M)).is_MatAdd

