
def test_DomainScalar_to_domain():
    A = DomainScalar(ZZ(1), ZZ)
    B = A.to_domain(QQ)
    assert B == DomainScalar(QQ(1), QQ)

