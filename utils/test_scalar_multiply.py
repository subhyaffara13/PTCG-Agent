
def test_scalar_multiply():
    assert SparseMatrix([[1, 2]]).scalar_multiply(3) == SparseMatrix([[3, 6]])

