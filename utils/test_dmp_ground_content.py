
def test_dmp_ground_content():
    assert dmp_ground_content([[]], 1, ZZ) == ZZ(0)
    assert dmp_ground_content([[]], 1, QQ) == QQ(0)
    assert dmp_ground_content([[1]], 1, ZZ) == ZZ(1)
    assert dmp_ground_content([[-1]], 1, ZZ) == ZZ(1)
    assert dmp_ground_content([[1], [1]], 1, ZZ) == ZZ(1)
    assert dmp_ground_content([[2], [2]], 1, ZZ) == ZZ(2)
    assert dmp_ground_content([[1], [2], [1]], 1, ZZ) == ZZ(1)
    assert dmp_ground_content([[2], [4], [2]], 1, ZZ) == ZZ(2)

    assert dmp_ground_content([[QQ(2, 3)], [QQ(4, 9)]], 1, QQ) == QQ(2, 9)
    assert dmp_ground_content([[QQ(2, 3)], [QQ(4, 5)]], 1, QQ) == QQ(2, 15)

    assert dmp_ground_content(f_0, 2, ZZ) == ZZ(1)
    assert dmp_ground_content(
        dmp_mul_ground(f_0, ZZ(2), 2, ZZ), 2, ZZ) == ZZ(2)

    assert dmp_ground_content(f_1, 2, ZZ) == ZZ(1)
    assert dmp_ground_content(
        dmp_mul_ground(f_1, ZZ(3), 2, ZZ), 2, ZZ) == ZZ(3)

    assert dmp_ground_content(f_2, 2, ZZ) == ZZ(1)
    assert dmp_ground_content(
        dmp_mul_ground(f_2, ZZ(4), 2, ZZ), 2, ZZ) == ZZ(4)

    assert dmp_ground_content(f_3, 2, ZZ) == ZZ(1)
    assert dmp_ground_content(
        dmp_mul_ground(f_3, ZZ(5), 2, ZZ), 2, ZZ) == ZZ(5)

    assert dmp_ground_content(f_4, 2, ZZ) == ZZ(1)
    assert dmp_ground_content(
        dmp_mul_ground(f_4, ZZ(6), 2, ZZ), 2, ZZ) == ZZ(6)

    assert dmp_ground_content(f_5, 2, ZZ) == ZZ(1)
    assert dmp_ground_content(
        dmp_mul_ground(f_5, ZZ(7), 2, ZZ), 2, ZZ) == ZZ(7)

    assert dmp_ground_content(f_6, 3, ZZ) == ZZ(1)
    assert dmp_ground_content(
        dmp_mul_ground(f_6, ZZ(8), 3, ZZ), 3, ZZ) == ZZ(8)

