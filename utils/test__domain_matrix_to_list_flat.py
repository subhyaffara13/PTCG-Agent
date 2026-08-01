
def test_DomainMatrix_to_list_flat():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    assert A.to_list_flat() == [ZZ(1), ZZ(2), ZZ(3), ZZ(4)]

