
def test_DDM_sub():
    A = DDM([[ZZ(1)], [ZZ(2)]], (2, 1), ZZ)
    B = DDM([[ZZ(3)], [ZZ(4)]], (2, 1), ZZ)
    C = DDM([[ZZ(-2)], [ZZ(-2)]], (2, 1), ZZ)
    AQ = DDM([[QQ(1)], [QQ(2)]], (2, 1), QQ)
    D = DDM([[ZZ(5)]], (1, 1), ZZ)
    assert A - B == A.sub(B) == C

    raises(TypeError, lambda: A - ZZ(1))
    raises(TypeError, lambda: ZZ(1) - A)
    raises(DMShapeError, lambda: A - D)
    raises(DMShapeError, lambda: D - A)
    raises(DMShapeError, lambda: A.sub(D))
    raises(DMShapeError, lambda: D.sub(A))
    raises(DMDomainError, lambda: A - AQ)
    raises(DMDomainError, lambda: AQ - A)
    raises(DMDomainError, lambda: A.sub(AQ))
    raises(DMDomainError, lambda: AQ.sub(A))

