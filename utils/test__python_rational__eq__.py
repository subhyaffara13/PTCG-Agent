
def test_PythonRational__eq__():
    assert (QQ(1, 2) == QQ(1, 2)) is True
    assert (QQ(1, 2) != QQ(1, 2)) is False

    assert (QQ(1, 2) == QQ(1, 3)) is False
    assert (QQ(1, 2) != QQ(1, 3)) is True

