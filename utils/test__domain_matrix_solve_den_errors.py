
def test_DomainMatrix_solve_den_errors():
    A = DomainMatrix([[ZZ(1), ZZ(2)]], (1, 2), ZZ)
    b = DomainMatrix([[ZZ(1)], [ZZ(2)]], (2, 1), ZZ)
    raises(DMShapeError, lambda: A.solve_den(b))
    raises(DMShapeError, lambda: A.solve_den_rref(b))

    A = DomainMatrix([[ZZ(1), ZZ(2)]], (1, 2), ZZ)
    b = DomainMatrix([[ZZ(1), ZZ(2)]], (1, 2), ZZ)
    raises(DMShapeError, lambda: A.solve_den(b))
    raises(DMShapeError, lambda: A.solve_den_rref(b))

    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    b1 = DomainMatrix([[ZZ(1), ZZ(2)]], (1, 2), ZZ)
    raises(DMShapeError, lambda: A.solve_den(b1))

    A = DomainMatrix([[ZZ(2)]], (1, 1), ZZ)
    b = DomainMatrix([[ZZ(2)]], (1, 1), ZZ)
    raises(DMBadInputError, lambda: A.solve_den(b1, method='invalid'))

    A = DomainMatrix([[ZZ(1)], [ZZ(2)]], (2, 1), ZZ)
    b = DomainMatrix([[ZZ(1)], [ZZ(2)]], (2, 1), ZZ)
    raises(DMNonSquareMatrixError, lambda: A.solve_den_charpoly(b))

