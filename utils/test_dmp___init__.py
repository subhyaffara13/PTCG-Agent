
def test_DMP___init__():
    f = DMP([[ZZ(0)], [], [ZZ(0), ZZ(1), ZZ(2)], [ZZ(3)]], ZZ)

    assert f._rep == [[1, 2], [3]]
    assert f.dom == ZZ
    assert f.lev == 1

    f = DMP([[ZZ(1), ZZ(2)], [ZZ(3)]], ZZ, 1)

    assert f._rep == [[1, 2], [3]]
    assert f.dom == ZZ
    assert f.lev == 1

    f = DMP.from_dict({(1, 1): ZZ(1), (0, 0): ZZ(2)}, 1, ZZ)

    assert f._rep == [[1, 0], [2]]
    assert f.dom == ZZ
    assert f.lev == 1

