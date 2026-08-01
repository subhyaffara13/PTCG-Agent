
def test_DomainMatrix_solve_den_rref_underdetermined():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(1), ZZ(2)]], (2, 2), ZZ)
    b = DomainMatrix([[ZZ(1)], [ZZ(1)]], (2, 1), ZZ)
    raises(DMNonInvertibleMatrixError, lambda: A.solve_den(b))
    raises(DMNonInvertibleMatrixError, lambda: A.solve_den_rref(b))

