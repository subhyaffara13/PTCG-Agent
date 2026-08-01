
def test_DomainMatrix_diag():
    A = DomainMatrix({0:{0:ZZ(2)}, 1:{1:ZZ(3)}}, (2, 2), ZZ)
    assert DomainMatrix.diag([ZZ(2), ZZ(3)], ZZ) == A

    A = DomainMatrix({0:{0:ZZ(2)}, 1:{1:ZZ(3)}}, (3, 4), ZZ)
    assert DomainMatrix.diag([ZZ(2), ZZ(3)], ZZ, (3, 4)) == A

