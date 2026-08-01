
def test_DomainScalar_eq():
    A = DomainScalar(QQ(2), QQ)
    assert A == A
    B = DomainScalar(ZZ(-5), ZZ)
    assert A != B
    C = DomainScalar(ZZ(2), ZZ)
    assert A != C
    D = [1]
    assert A != D

