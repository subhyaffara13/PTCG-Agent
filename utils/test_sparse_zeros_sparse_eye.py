
def test_sparse_zeros_sparse_eye():
    assert SparseMatrix.eye(3) == eye(3, cls=SparseMatrix)
    assert len(SparseMatrix.eye(3).todok()) == 3
    assert SparseMatrix.zeros(3) == zeros(3, cls=SparseMatrix)
    assert len(SparseMatrix.zeros(3).todok()) == 0

