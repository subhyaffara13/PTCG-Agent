
def test_SDM_neg():
    A = SDM({0:{1:ZZ(1)}, 1:{0:ZZ(2), 1:ZZ(3)}}, (2, 2), ZZ)
    B = SDM({0:{1:ZZ(-1)}, 1:{0:ZZ(-2), 1:ZZ(-3)}}, (2, 2), ZZ)
    assert A.neg() == -A == B

