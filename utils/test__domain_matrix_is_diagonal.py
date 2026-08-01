
def test_DomainMatrix_is_diagonal():
    A = DM([[1, 0], [0, 4]], ZZ)
    B = DM([[1, 2], [3, 4]], ZZ)
    assert A.is_diagonal is A.to_sparse().is_diagonal is True
    assert B.is_diagonal is B.to_sparse().is_diagonal is False

