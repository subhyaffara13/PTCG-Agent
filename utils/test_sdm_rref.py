
def test_sdm_rref(name, A, A_rref, den):
    A = A.to_field().to_sdm()
    _check_divide(A.rref(), A_rref, den)


def test_SDM_rref():
    # More tests are in test_rref.py

    A = SDM({0:{0:QQ(1), 1:QQ(2)},
             1:{0:QQ(3), 1:QQ(4)}}, (2, 2), QQ)
    A_rref = SDM({0:{0:QQ(1)}, 1:{1:QQ(1)}}, (2, 2), QQ)
    assert A.rref() == (A_rref, [0, 1])

    A = SDM({0: {0: QQ(1), 1: QQ(2), 2: QQ(2)},
             1: {0: QQ(3),           2: QQ(4)}}, (2, 3), ZZ)
    A_rref = SDM({0: {0: QQ(1,1), 2: QQ(4,3)},
                  1: {1: QQ(1,1), 2: QQ(1,3)}}, (2, 3), QQ)
    assert A.rref() == (A_rref, [0, 1])

