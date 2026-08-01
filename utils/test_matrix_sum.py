
def test_matrix_sum():
    A = Matrix([[0, 1], [n, 0]])

    result = Sum(A, (n, 0, 3)).doit()
    assert result == Matrix([[0, 4], [6, 0]])
    assert result.__class__ == ImmutableDenseMatrix

    A = SparseMatrix([[0, 1], [n, 0]])

    result = Sum(A, (n, 0, 3)).doit()
    assert result.__class__ == ImmutableSparseMatrix

