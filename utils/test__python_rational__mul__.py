
def test_PythonRational__mul__():
    assert QQ(-1, 2) * QQ( 1, 2) == QQ(-1, 4)
    assert QQ( 1, 2) * QQ(-1, 2) == QQ(-1, 4)

    assert QQ(1, 2) * QQ(1, 2) == QQ(1, 4)
    assert QQ(1, 2) * QQ(3, 2) == QQ(3, 4)
    assert QQ(3, 2) * QQ(1, 2) == QQ(3, 4)
    assert QQ(3, 2) * QQ(3, 2) == QQ(9, 4)

    assert 2 * QQ(1, 2) == QQ(1)
    assert QQ(1, 2) * 2 == QQ(1)

