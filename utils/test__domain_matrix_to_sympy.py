
def test_DomainMatrix_to_sympy():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    assert A.to_sympy() == A.convert_to(EXRAW)

