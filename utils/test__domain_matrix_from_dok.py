
def test_DomainMatrix_from_dok():
    items = {(0, 0): ZZ(1), (1, 1): ZZ(2)}
    A = DM([[1, 0], [0, 2]], ZZ)
    assert DomainMatrix.from_dok(items, (2, 2), ZZ) == A.to_sparse()
    assert DDM.from_dok(items, (2, 2), ZZ) == A.rep.to_ddm()
    assert SDM.from_dok(items, (2, 2), ZZ) == A.rep.to_sdm()

