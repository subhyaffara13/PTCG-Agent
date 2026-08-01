
def test_sparse_creation():
    a = SparseMatrix(2, 2, {(0, 0): [[1, 2], [3, 4]]})
    assert a == SparseMatrix([[1, 2], [3, 4]])
    a = SparseMatrix(2, 2, {(0, 0): [[1, 2]]})
    assert a == SparseMatrix([[1, 2], [0, 0]])
    a = SparseMatrix(2, 2, {(0, 0): [1, 2]})
    assert a == SparseMatrix([[1, 0], [2, 0]])

