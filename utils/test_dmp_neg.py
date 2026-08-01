
def test_dmp_neg():
    assert dmp_neg([ZZ(-1)], 0, ZZ) == [ZZ(1)]
    assert dmp_neg([QQ(-1, 2)], 0, QQ) == [QQ(1, 2)]

    assert dmp_neg([[[]]], 2, ZZ) == [[[]]]
    assert dmp_neg([[[ZZ(1)]]], 2, ZZ) == [[[ZZ(-1)]]]
    assert dmp_neg([[[ZZ(-7)]]], 2, ZZ) == [[[ZZ(7)]]]

    assert dmp_neg([[[]]], 2, QQ) == [[[]]]
    assert dmp_neg([[[QQ(1, 9)]]], 2, QQ) == [[[QQ(-1, 9)]]]
    assert dmp_neg([[[QQ(-7, 9)]]], 2, QQ) == [[[QQ(7, 9)]]]

