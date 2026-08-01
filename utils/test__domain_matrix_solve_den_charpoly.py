
def test_DomainMatrix_solve_den_charpoly():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    b = DomainMatrix([[ZZ(1)], [ZZ(2)]], (2, 1), ZZ)
    A1 = DomainMatrix([[ZZ(1), ZZ(2)]], (1, 2), ZZ)
    raises(DMNonSquareMatrixError, lambda: A1.solve_den_charpoly(b))
    b1 = DomainMatrix([[ZZ(1), ZZ(2)]], (1, 2), ZZ)
    raises(DMShapeError, lambda: A.solve_den_charpoly(b1))
    bq = DomainMatrix([[QQ(1)], [QQ(2)]], (2, 1), QQ)
    raises(DMDomainError, lambda: A.solve_den_charpoly(bq))

