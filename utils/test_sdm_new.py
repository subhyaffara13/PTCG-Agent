
def test_SDM_new():
    A = SDM({0:{0:ZZ(1)}}, (2, 2), ZZ)
    B = A.new({}, (2, 2), ZZ)
    assert B == SDM({}, (2, 2), ZZ)

