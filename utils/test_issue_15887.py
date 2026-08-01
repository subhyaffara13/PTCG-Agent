
def test_issue_15887():
    # Mutable matrix should not use cache
    a = MutableDenseMatrix([[0, 1], [1, 0]])
    assert a.is_diagonalizable() is True
    a[1, 0] = 0
    assert a.is_diagonalizable() is False

    a = MutableDenseMatrix([[0, 1], [1, 0]])
    a.diagonalize()
    a[1, 0] = 0
    raises(MatrixError, lambda: a.diagonalize())


def test_issue_15887():
    # Mutable matrix should not use cache
    a = MutableDenseMatrix([[0, 1], [1, 0]])
    assert a.is_diagonalizable() is True
    a[1, 0] = 0
    assert a.is_diagonalizable() is False

    a = MutableDenseMatrix([[0, 1], [1, 0]])
    a.diagonalize()
    a[1, 0] = 0
    raises(MatrixError, lambda: a.diagonalize())

