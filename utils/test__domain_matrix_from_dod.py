
def test_DomainMatrix_from_dod():
    items = {0: {0: ZZ(1), 1:ZZ(2)}, 1: {0:ZZ(3), 1:ZZ(4)}}
    A = DM([[1, 2], [3, 4]], ZZ)
    assert DomainMatrix.from_dod(items, (2, 2), ZZ) == A.to_sparse()
    assert A.from_dod_like(items) == A
    assert A.from_dod_like(items, QQ) == A.convert_to(QQ)

