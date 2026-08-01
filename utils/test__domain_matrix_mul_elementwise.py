
def test_DomainMatrix_mul_elementwise():
    A = DomainMatrix([[ZZ(2), ZZ(2)], [ZZ(0), ZZ(0)]], (2, 2), ZZ)
    B = DomainMatrix([[ZZ(4), ZZ(0)], [ZZ(3), ZZ(0)]], (2, 2), ZZ)
    C = DomainMatrix([[ZZ(8), ZZ(0)], [ZZ(0), ZZ(0)]], (2, 2), ZZ)
    assert A.mul_elementwise(B) == C
    assert B.mul_elementwise(A) == C

