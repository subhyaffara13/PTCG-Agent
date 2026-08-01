
def test_SDM_is_zero_matrix():
    A = SDM({0: {0: QQ(1)}}, (2, 2), QQ)
    Azero = SDM.zeros((1, 2), QQ)
    assert A.is_zero_matrix() is False
    assert Azero.is_zero_matrix() is True

