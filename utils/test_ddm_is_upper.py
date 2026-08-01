
def test_DDM_is_upper():
    # Wide matrices:
    A = DDM([
        [QQ(1), QQ(2), QQ(3), QQ(4)],
        [QQ(0), QQ(5), QQ(6), QQ(7)],
        [QQ(0), QQ(0), QQ(8), QQ(9)]
    ], (3, 4), QQ)
    B = DDM([
        [QQ(1), QQ(2), QQ(3), QQ(4)],
        [QQ(0), QQ(5), QQ(6), QQ(7)],
        [QQ(0), QQ(7), QQ(8), QQ(9)]
    ], (3, 4), QQ)
    assert A.is_upper() is True
    assert B.is_upper() is False

    # Tall matrices:
    A = DDM([
        [QQ(1), QQ(2), QQ(3)],
        [QQ(0), QQ(5), QQ(6)],
        [QQ(0), QQ(0), QQ(8)],
        [QQ(0), QQ(0), QQ(0)]
    ], (4, 3), QQ)
    B = DDM([
        [QQ(1), QQ(2), QQ(3)],
        [QQ(0), QQ(5), QQ(6)],
        [QQ(0), QQ(0), QQ(8)],
        [QQ(0), QQ(0), QQ(10)]
    ], (4, 3), QQ)
    assert A.is_upper() is True
    assert B.is_upper() is False

