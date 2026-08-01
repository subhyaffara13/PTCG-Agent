
def test_DomainMatrix_applyfunc():
    A = DomainMatrix([[ZZ(1), ZZ(2)]], (1, 2), ZZ)
    B = DomainMatrix([[ZZ(2), ZZ(4)]], (1, 2), ZZ)
    assert A.applyfunc(lambda x: 2*x) == B

