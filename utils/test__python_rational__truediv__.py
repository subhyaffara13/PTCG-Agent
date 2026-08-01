
def test_PythonRational__truediv__():
    assert QQ(-1, 2) / QQ( 1, 2) == QQ(-1)
    assert QQ( 1, 2) / QQ(-1, 2) == QQ(-1)

    assert QQ(1, 2) / QQ(1, 2) == QQ(1)
    assert QQ(1, 2) / QQ(3, 2) == QQ(1, 3)
    assert QQ(3, 2) / QQ(1, 2) == QQ(3)
    assert QQ(3, 2) / QQ(3, 2) == QQ(1)

    assert 2 / QQ(1, 2) == QQ(4)
    assert QQ(1, 2) / 2 == QQ(1, 4)

    raises(ZeroDivisionError, lambda: QQ(1, 2) / QQ(0))
    raises(ZeroDivisionError, lambda: QQ(1, 2) / 0)

