
def test_dup_primitive():
    assert dup_primitive([], ZZ) == (ZZ(0), [])
    assert dup_primitive([ZZ(1)], ZZ) == (ZZ(1), [ZZ(1)])
    assert dup_primitive([ZZ(1), ZZ(1)], ZZ) == (ZZ(1), [ZZ(1), ZZ(1)])
    assert dup_primitive([ZZ(2), ZZ(2)], ZZ) == (ZZ(2), [ZZ(1), ZZ(1)])
    assert dup_primitive(
        [ZZ(1), ZZ(2), ZZ(1)], ZZ) == (ZZ(1), [ZZ(1), ZZ(2), ZZ(1)])
    assert dup_primitive(
        [ZZ(2), ZZ(4), ZZ(2)], ZZ) == (ZZ(2), [ZZ(1), ZZ(2), ZZ(1)])

    assert dup_primitive([], QQ) == (QQ(0), [])
    assert dup_primitive([QQ(1)], QQ) == (QQ(1), [QQ(1)])
    assert dup_primitive([QQ(1), QQ(1)], QQ) == (QQ(1), [QQ(1), QQ(1)])
    assert dup_primitive([QQ(2), QQ(2)], QQ) == (QQ(2), [QQ(1), QQ(1)])
    assert dup_primitive(
        [QQ(1), QQ(2), QQ(1)], QQ) == (QQ(1), [QQ(1), QQ(2), QQ(1)])
    assert dup_primitive(
        [QQ(2), QQ(4), QQ(2)], QQ) == (QQ(2), [QQ(1), QQ(2), QQ(1)])

    assert dup_primitive(
        [QQ(2, 3), QQ(4, 9)], QQ) == (QQ(2, 9), [QQ(3), QQ(2)])
    assert dup_primitive(
        [QQ(2, 3), QQ(4, 5)], QQ) == (QQ(2, 15), [QQ(5), QQ(6)])

