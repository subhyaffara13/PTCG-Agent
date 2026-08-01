
def test_sdm_inv(name, A, A_inv, den):
    A = A.to_field().to_sdm()
    if den != 0:
        A_inv = (A_inv.to_field() / den).to_sdm()
        assert A.inv() == A_inv
    else:
        raises(DMNonInvertibleMatrixError, lambda: A.inv())


def test_SDM_inv():
    A = SDM({0:{0:QQ(1), 1:QQ(2)}, 1:{0:QQ(3), 1:QQ(4)}}, (2, 2), QQ)
    B = SDM({0:{0:QQ(-2), 1:QQ(1)}, 1:{0:QQ(3, 2), 1:QQ(-1, 2)}}, (2, 2), QQ)
    assert A.inv() == B

