
def test_DomainMatrix_to_dod():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    assert A.to_dod() == {0: {0: ZZ(1), 1:ZZ(2)}, 1: {0:ZZ(3), 1:ZZ(4)}}
    A = DomainMatrix([[ZZ(1), ZZ(0)], [ZZ(0), ZZ(4)]], (2, 2), ZZ)
    assert A.to_dod() == {0: {0: ZZ(1)}, 1: {1: ZZ(4)}}

