
def test_BlockMatrix_2x2_inverse_symbolic():
    A = MatrixSymbol('A', n, m)
    B = MatrixSymbol('B', n, k - m)
    C = MatrixSymbol('C', k - n, m)
    D = MatrixSymbol('D', k - n, k - m)
    X = BlockMatrix([[A, B], [C, D]])
    assert X.is_square and X.shape == (k, k)
    assert isinstance(block_collapse(X.I), Inverse)  # Can't invert when none of the blocks is square

    # test code path where only A is invertible
    A = MatrixSymbol('A', n, n)
    B = MatrixSymbol('B', n, m)
    C = MatrixSymbol('C', m, n)
    D = ZeroMatrix(m, m)
    X = BlockMatrix([[A, B], [C, D]])
    assert block_collapse(X.inverse()) == BlockMatrix([
        [A.I + A.I * B * X.schur('A').I * C * A.I, -A.I * B * X.schur('A').I],
        [-X.schur('A').I * C * A.I, X.schur('A').I],
    ])

    # test code path where only B is invertible
    A = MatrixSymbol('A', n, m)
    B = MatrixSymbol('B', n, n)
    C = ZeroMatrix(m, m)
    D = MatrixSymbol('D', m, n)
    X = BlockMatrix([[A, B], [C, D]])
    assert block_collapse(X.inverse()) == BlockMatrix([
        [-X.schur('B').I * D * B.I, X.schur('B').I],
        [B.I + B.I * A * X.schur('B').I * D * B.I, -B.I * A * X.schur('B').I],
    ])

    # test code path where only C is invertible
    A = MatrixSymbol('A', n, m)
    B = ZeroMatrix(n, n)
    C = MatrixSymbol('C', m, m)
    D = MatrixSymbol('D', m, n)
    X = BlockMatrix([[A, B], [C, D]])
    assert block_collapse(X.inverse()) == BlockMatrix([
        [-C.I * D * X.schur('C').I, C.I + C.I * D * X.schur('C').I * A * C.I],
        [X.schur('C').I, -X.schur('C').I * A * C.I],
    ])

    # test code path where only D is invertible
    A = ZeroMatrix(n, n)
    B = MatrixSymbol('B', n, m)
    C = MatrixSymbol('C', m, n)
    D = MatrixSymbol('D', m, m)
    X = BlockMatrix([[A, B], [C, D]])
    assert block_collapse(X.inverse()) == BlockMatrix([
        [X.schur('D').I, -X.schur('D').I * B * D.I],
        [-D.I * C * X.schur('D').I, D.I + D.I * C * X.schur('D').I * B * D.I],
    ])

