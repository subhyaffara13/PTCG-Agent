
def test_Submodule_mul():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    C = A.submodule_from_matrix(DomainMatrix([
        [0, 10, 0, 0],
        [0, 0, 7, 0],
    ], (2, 4), ZZ).transpose(), denom=15)
    C1 = A.submodule_from_matrix(DomainMatrix([
        [0, 20, 0, 0],
        [0, 0, 14, 0],
    ], (2, 4), ZZ).transpose(), denom=3)
    C2 = A.submodule_from_matrix(DomainMatrix([
        [0, 0, 10, 0],
        [0, 0,  0, 7],
    ], (2, 4), ZZ).transpose(), denom=15)
    C3_unred = A.submodule_from_matrix(DomainMatrix([
        [0, 0, 100, 0],
        [0, 0, 0, 70],
        [0, 0, 0, 70],
        [-49, -49, -49, -49]
    ], (4, 4), ZZ).transpose(), denom=225)
    C3 = A.submodule_from_matrix(DomainMatrix([
        [4900, 4900, 0, 0],
        [4410, 4410, 10, 0],
        [2107, 2107, 7, 7]
    ], (3, 4), ZZ).transpose(), denom=225)
    assert C * 1 == C
    assert C ** 1 == C
    assert C * 10 == C1
    assert C * A(1) == C2
    assert C.mul(C, hnf=False) == C3_unred
    assert C * C == C3
    assert C ** 2 == C3

