
def test_DomainMatrix_diagonal():
    A = DM([[1, 2], [3, 4]], ZZ)
    assert A.diagonal() == A.to_sparse().diagonal() == [ZZ(1), ZZ(4)]
    A = DM([[1, 2], [3, 4], [5, 6]], ZZ)
    assert A.diagonal() == A.to_sparse().diagonal() == [ZZ(1), ZZ(4)]
    A = DM([[1, 2, 3], [4, 5, 6]], ZZ)
    assert A.diagonal() == A.to_sparse().diagonal() == [ZZ(1), ZZ(5)]

