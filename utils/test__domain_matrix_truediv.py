
def test_DomainMatrix_truediv():
    A = DomainMatrix.from_Matrix(Matrix([[1, 2], [3, 4]]))
    lamda = DomainScalar(QQ(3)/QQ(2), QQ)
    assert A / lamda == DomainMatrix({0: {0: QQ(2, 3), 1: QQ(4, 3)}, 1: {0: QQ(2), 1: QQ(8, 3)}}, (2, 2), QQ)
    b = DomainScalar(ZZ(1), ZZ)
    assert A / b == DomainMatrix({0: {0: QQ(1), 1: QQ(2)}, 1: {0: QQ(3), 1: QQ(4)}}, (2, 2), QQ)

    assert A / 1 == DomainMatrix({0: {0: QQ(1), 1: QQ(2)}, 1: {0: QQ(3), 1: QQ(4)}}, (2, 2), QQ)
    assert A / 2 == DomainMatrix({0: {0: QQ(1, 2), 1: QQ(1)}, 1: {0: QQ(3, 2), 1: QQ(2)}}, (2, 2), QQ)

    raises(ZeroDivisionError, lambda: A / 0)
    raises(TypeError, lambda: A / 1.5)
    raises(ZeroDivisionError, lambda: A / DomainScalar(ZZ(0), ZZ))

    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    assert A.to_field() / 2 == DomainMatrix([[QQ(1, 2), QQ(1)], [QQ(3, 2), QQ(2)]], (2, 2), QQ)
    assert A / 2 == DomainMatrix([[QQ(1, 2), QQ(1)], [QQ(3, 2), QQ(2)]], (2, 2), QQ)
    assert A.to_field() / QQ(2,3) == DomainMatrix([[QQ(3, 2), QQ(3)], [QQ(9, 2), QQ(6)]], (2, 2), QQ)

