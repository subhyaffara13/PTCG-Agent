
def test_DomainMatrix_is_square():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    B = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)], [ZZ(5), ZZ(6)]], (3, 2), ZZ)
    assert A.is_square is True
    assert B.is_square is False

