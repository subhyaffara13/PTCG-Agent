
def test_GaussianRational():
    assert str(QQ_I(1, 0)) == "1"
    assert str(QQ_I(QQ(2, 3), 0)) == "2/3"
    assert str(QQ_I(0, QQ(2, 3))) == "2*I/3"
    assert str(QQ_I(QQ(1, 2), QQ(-2, 3))) == "1/2 - 2*I/3"

