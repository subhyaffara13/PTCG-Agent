
def test_SparseMatrices():
    assert maple_code(SparseMatrix(Identity(2))) == 'Matrix([[1, 0], [0, 1]], storage = sparse)'

