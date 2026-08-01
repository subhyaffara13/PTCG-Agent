
def test_DomainMatrix_inv_den():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    den = ZZ(-2)
    result = DomainMatrix([[ZZ(4), ZZ(-2)], [ZZ(-3), ZZ(1)]], (2, 2), ZZ)
    assert A.inv_den() == (result, den)

