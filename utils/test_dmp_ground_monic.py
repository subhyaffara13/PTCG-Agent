
def test_dmp_ground_monic():
    assert dmp_ground_monic([3, 6, 9], 0, ZZ) == [1, 2, 3]

    assert dmp_ground_monic([[3], [6], [9]], 1, ZZ) == [[1], [2], [3]]

    raises(
        ExactQuotientFailed, lambda: dmp_ground_monic([[3], [4], [5]], 1, ZZ))

    assert dmp_ground_monic([[]], 1, QQ) == [[]]
    assert dmp_ground_monic([[QQ(1)]], 1, QQ) == [[QQ(1)]]
    assert dmp_ground_monic(
        [[QQ(7)], [QQ(1)], [QQ(21)]], 1, QQ) == [[QQ(1)], [QQ(1, 7)], [QQ(3)]]

