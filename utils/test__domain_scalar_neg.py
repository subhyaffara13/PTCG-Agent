
def test_DomainScalar_neg():
    A = DomainScalar(QQ(2), QQ)
    B = DomainScalar(QQ(-2), QQ)
    assert  -A == B

