
def test_DomainMatrix_from_list():
    ddm = DDM([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    A = DomainMatrix.from_list([[1, 2], [3, 4]], ZZ)
    if GROUND_TYPES != 'flint':
        assert A.rep == ddm
    else:
        assert A.rep == ddm.to_dfm()
    assert A.shape == (2, 2)
    assert A.domain == ZZ

    dom = FF(7)
    ddm = DDM([[dom(1), dom(2)], [dom(3), dom(4)]], (2, 2), dom)
    A = DomainMatrix.from_list([[1, 2], [3, 4]], dom)
    if GROUND_TYPES != 'flint':
        assert A.rep == ddm
    else:
        assert A.rep == ddm.to_dfm()
    assert A.shape == (2, 2)
    assert A.domain == dom

    dom = FF(2**127-1)
    ddm = DDM([[dom(1), dom(2)], [dom(3), dom(4)]], (2, 2), dom)
    A = DomainMatrix.from_list([[1, 2], [3, 4]], dom)
    if GROUND_TYPES != 'flint':
        assert A.rep == ddm
    else:
        assert A.rep == ddm.to_dfm()
    assert A.shape == (2, 2)
    assert A.domain == dom

    ddm = DDM([[QQ(1, 2), QQ(3, 1)], [QQ(1, 4), QQ(5, 1)]], (2, 2), QQ)
    A = DomainMatrix.from_list([[(1, 2), (3, 1)], [(1, 4), (5, 1)]], QQ)
    if GROUND_TYPES != 'flint':
        assert A.rep == ddm
    else:
        assert A.rep == ddm.to_dfm()
    assert A.shape == (2, 2)
    assert A.domain == QQ

