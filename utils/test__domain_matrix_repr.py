
def test_DomainMatrix_repr():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    assert repr(A) == 'DomainMatrix([[1, 2], [3, 4]], (2, 2), ZZ)'

