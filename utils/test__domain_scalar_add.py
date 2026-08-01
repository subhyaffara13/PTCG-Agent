
def test_DomainScalar_add():
    A = DomainScalar(ZZ(1), ZZ)
    B = DomainScalar(QQ(2), QQ)
    assert A + B == DomainScalar(QQ(3), QQ)

    raises(TypeError, lambda: A + 1.5)

