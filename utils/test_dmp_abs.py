
def test_dmp_abs():
    assert dmp_abs([ZZ(-1)], 0, ZZ) == [ZZ(1)]
    assert dmp_abs([QQ(-1, 2)], 0, QQ) == [QQ(1, 2)]

    assert dmp_abs([[[]]], 2, ZZ) == [[[]]]
    assert dmp_abs([[[ZZ(1)]]], 2, ZZ) == [[[ZZ(1)]]]
    assert dmp_abs([[[ZZ(-7)]]], 2, ZZ) == [[[ZZ(7)]]]

    assert dmp_abs([[[]]], 2, QQ) == [[[]]]
    assert dmp_abs([[[QQ(1, 2)]]], 2, QQ) == [[[QQ(1, 2)]]]
    assert dmp_abs([[[QQ(-7, 9)]]], 2, QQ) == [[[QQ(7, 9)]]]

