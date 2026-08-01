
def test_addition():
    a = Matrix((
        (1, 2),
        (3, 1),
    ))

    b = Matrix((
        (1, 2),
        (3, 0),
    ))

    assert a + b == a.add(b) == Matrix([[2, 4], [6, 1]])


def test_addition():
    a = Matrix((
        (1, 2),
        (3, 1),
    ))

    b = Matrix((
        (1, 2),
        (3, 0),
    ))

    assert a + b == a.add(b) == Matrix([[2, 4], [6, 1]])


def test_addition():
    A = MatrixSymbol('A', n, m)
    B = MatrixSymbol('B', n, m)

    assert isinstance(A + B, MatAdd)
    assert (A + B).shape == A.shape
    assert isinstance(A - A + 2*B, MatMul)

    raises(TypeError, lambda: A + 1)
    raises(TypeError, lambda: 5 + A)
    raises(TypeError, lambda: 5 - A)

    assert A + ZeroMatrix(n, m) - A == ZeroMatrix(n, m)
    raises(TypeError, lambda: ZeroMatrix(n, m) + S.Zero)

