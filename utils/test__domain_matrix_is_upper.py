
def test_DomainMatrix_is_upper():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(0), ZZ(4)]], (2, 2), ZZ)
    B = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    assert A.is_upper is True
    assert B.is_upper is False

