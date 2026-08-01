
def test_PythonRational__lt_le_gt_ge__():
    assert (QQ(1, 2) < QQ(1, 4)) is False
    assert (QQ(1, 2) <= QQ(1, 4)) is False
    assert (QQ(1, 2) > QQ(1, 4)) is True
    assert (QQ(1, 2) >= QQ(1, 4)) is True

    assert (QQ(1, 4) < QQ(1, 2)) is True
    assert (QQ(1, 4) <= QQ(1, 2)) is True
    assert (QQ(1, 4) > QQ(1, 2)) is False
    assert (QQ(1, 4) >= QQ(1, 2)) is False

