
def test_SDM_transpose():
    A = SDM({0:{0:ZZ(1), 1:ZZ(2)}, 1:{0:ZZ(3), 1:ZZ(4)}}, (2, 2), ZZ)
    B = SDM({0:{0:ZZ(1), 1:ZZ(3)}, 1:{0:ZZ(2), 1:ZZ(4)}}, (2, 2), ZZ)
    assert A.transpose() == B

    A = SDM({0:{1:ZZ(2)}}, (2, 2), ZZ)
    B = SDM({1:{0:ZZ(2)}}, (2, 2), ZZ)
    assert A.transpose() == B

    A = SDM({0:{1:ZZ(2)}}, (1, 2), ZZ)
    B = SDM({1:{0:ZZ(2)}}, (2, 1), ZZ)
    assert A.transpose() == B

