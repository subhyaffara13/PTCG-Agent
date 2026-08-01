
def test_SDM_is_lower():
    A = SDM({0: {0: QQ(1), 1: QQ(2), 2: QQ(3), 3: QQ(4)},
                       1: {1: QQ(5), 2: QQ(6), 3: QQ(7)},
                                 2: {2: QQ(8), 3: QQ(9)}}, (3, 4), QQ
            ).transpose()
    B = SDM({0: {0: QQ(1), 1: QQ(2), 2: QQ(3), 3: QQ(4)},
                       1: {1: QQ(5), 2: QQ(6), 3: QQ(7)},
                       2: {1: QQ(7), 2: QQ(8), 3: QQ(9)}}, (3, 4), QQ
            ).transpose()
    assert A.is_lower() is True
    assert B.is_lower() is False

