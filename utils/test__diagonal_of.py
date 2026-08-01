
def test_DiagonalOf():
    x = MatrixSymbol('x', n, n)
    d = DiagonalOf(x)
    assert d.shape == (n, 1)
    assert d.diagonal_length == n
    assert d[2, 0] == d[2] == x[2, 2]

    x = MatrixSymbol('x', n, m)
    d = DiagonalOf(x)
    assert d.shape == (None, 1)
    assert d.diagonal_length is None
    assert d[2, 0] == d[2] == x[2, 2]

    d = DiagonalOf(MatrixSymbol('x', 4, 3))
    assert d.shape == (3, 1)
    d = DiagonalOf(MatrixSymbol('x', n, 3))
    assert d.shape == (3, 1)
    d = DiagonalOf(MatrixSymbol('x', 3, n))
    assert d.shape == (3, 1)
    x = MatrixSymbol('x', n, m)
    assert [DiagonalOf(x)[i] for i in range(4)] ==[
        x[0, 0], x[1, 1], x[2, 2], x[3, 3]]

