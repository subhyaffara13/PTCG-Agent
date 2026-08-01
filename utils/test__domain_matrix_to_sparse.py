
def test_DomainMatrix_to_sparse():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    A_sparse = A.to_sparse()
    assert A_sparse.rep == {0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}}

