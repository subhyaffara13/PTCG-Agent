
def test_DomainMatrix_eq():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    assert A == A
    B = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(1)]], (2, 2), ZZ)
    assert A != B
    C = [[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]]
    assert A != C

