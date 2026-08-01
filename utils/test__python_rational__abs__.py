
def test_PythonRational__abs__():
    assert abs(QQ(-1, 2)) == QQ(1, 2)
    assert abs(QQ( 1, 2)) == QQ(1, 2)

