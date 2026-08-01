
def test_dmp_integrate():
    assert dmp_integrate([QQ(1)], 2, 0, QQ) == [QQ(1, 2), QQ(0), QQ(0)]

    assert dmp_integrate([[[]]], 1, 2, QQ) == [[[]]]
    assert dmp_integrate([[[]]], 2, 2, QQ) == [[[]]]

    assert dmp_integrate([[[QQ(1)]]], 1, 2, QQ) == [[[QQ(1)]], [[]]]
    assert dmp_integrate([[[QQ(1)]]], 2, 2, QQ) == [[[QQ(1, 2)]], [[]], [[]]]

    assert dmp_integrate([[QQ(1)], [QQ(2)], [QQ(3)]], 0, 1, QQ) == \
        [[QQ(1)], [QQ(2)], [QQ(3)]]
    assert dmp_integrate([[QQ(1)], [QQ(2)], [QQ(3)]], 1, 1, QQ) == \
        [[QQ(1, 3)], [QQ(1)], [QQ(3)], []]
    assert dmp_integrate([[QQ(1)], [QQ(2)], [QQ(3)]], 2, 1, QQ) == \
        [[QQ(1, 12)], [QQ(1, 3)], [QQ(3, 2)], [], []]
    assert dmp_integrate([[QQ(1)], [QQ(2)], [QQ(3)]], 3, 1, QQ) == \
        [[QQ(1, 60)], [QQ(1, 12)], [QQ(1, 2)], [], [], []]

