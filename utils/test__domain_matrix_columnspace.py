
def test_DomainMatrix_columnspace():
    A = DomainMatrix([[QQ(1), QQ(-1), QQ(1)], [QQ(2), QQ(-2), QQ(3)]], (2, 3), QQ)
    Acol = DomainMatrix([[QQ(1), QQ(1)], [QQ(2), QQ(3)]], (2, 2), QQ)
    assert A.columnspace() == Acol

    Az = DomainMatrix([[ZZ(1), ZZ(-1), ZZ(1)], [ZZ(2), ZZ(-2), ZZ(3)]], (2, 3), ZZ)
    raises(DMNotAField, lambda: Az.columnspace())

    A = DomainMatrix([[QQ(1), QQ(-1), QQ(1)], [QQ(2), QQ(-2), QQ(3)]], (2, 3), QQ, fmt='sparse')
    Acol = DomainMatrix({0: {0: QQ(1), 1: QQ(1)}, 1: {0: QQ(2), 1: QQ(3)}}, (2, 2), QQ)
    assert A.columnspace() == Acol

