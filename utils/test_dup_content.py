
def test_dup_content():
    assert dup_content([], ZZ) == ZZ(0)
    assert dup_content([1], ZZ) == ZZ(1)
    assert dup_content([-1], ZZ) == ZZ(1)
    assert dup_content([1, 1], ZZ) == ZZ(1)
    assert dup_content([2, 2], ZZ) == ZZ(2)
    assert dup_content([1, 2, 1], ZZ) == ZZ(1)
    assert dup_content([2, 4, 2], ZZ) == ZZ(2)

    assert dup_content([QQ(2, 3), QQ(4, 9)], QQ) == QQ(2, 9)
    assert dup_content([QQ(2, 3), QQ(4, 5)], QQ) == QQ(2, 15)

