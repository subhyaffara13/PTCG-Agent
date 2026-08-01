
def test_squareBlockMatrix():
    A = MatrixSymbol('A', n, n)
    B = MatrixSymbol('B', n, m)
    C = MatrixSymbol('C', m, n)
    D = MatrixSymbol('D', m, m)
    X = BlockMatrix([[A, B], [C, D]])
    Y = BlockMatrix([[A]])

    assert X.is_square

    Q = X + Identity(m + n)
    assert (block_collapse(Q) ==
        BlockMatrix([[A + Identity(n), B], [C, D + Identity(m)]]))

    assert (X + MatrixSymbol('Q', n + m, n + m)).is_MatAdd
    assert (X * MatrixSymbol('Q', n + m, n + m)).is_MatMul

    assert block_collapse(Y.I) == A.I

    assert isinstance(X.inverse(), Inverse)

    assert not X.is_Identity

    Z = BlockMatrix([[Identity(n), B], [C, D]])
    assert not Z.is_Identity

