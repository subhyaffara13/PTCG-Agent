
def test_DomainMatrix_flat():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    assert A.flat() == [ZZ(1), ZZ(2), ZZ(3), ZZ(4)]

