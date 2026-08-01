
def test_DomainMatrix_solve_den_charpoly_check():
    # Test check
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(2), ZZ(4)]], (2, 2), ZZ)
    b = DomainMatrix([[ZZ(1)], [ZZ(3)]], (2, 1), ZZ)
    raises(DMNonInvertibleMatrixError, lambda: A.solve_den_charpoly(b))
    adjAb = DomainMatrix([[ZZ(-2)], [ZZ(1)]], (2, 1), ZZ)
    assert A.adjugate() * b == adjAb
    assert A.solve_den_charpoly(b, check=False) == (adjAb, ZZ(0))

