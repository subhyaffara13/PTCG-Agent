
def test_DomainMatrix_to_dok():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    assert A.to_dok() == {(0, 0):ZZ(1), (0, 1):ZZ(2), (1, 0):ZZ(3), (1, 1):ZZ(4)}
    A = DomainMatrix([[ZZ(1), ZZ(0)], [ZZ(0), ZZ(4)]], (2, 2), ZZ)
    dok = {(0, 0):ZZ(1), (1, 1):ZZ(4)}
    assert A.to_dok() == dok
    assert A.to_dense().to_dok() == dok
    assert A.to_sparse().to_dok() == dok
    assert A.rep.to_ddm().to_dok() == dok
    assert A.rep.to_sdm().to_dok() == dok

