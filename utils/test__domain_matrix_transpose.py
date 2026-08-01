
def test_DomainMatrix_transpose():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    AT = DomainMatrix([[ZZ(1), ZZ(3)], [ZZ(2), ZZ(4)]], (2, 2), ZZ)
    assert A.transpose() == AT

