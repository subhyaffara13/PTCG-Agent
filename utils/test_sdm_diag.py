
def test_SDM_diag():
    A = SDM.diag([ZZ(1), ZZ(2)], ZZ, (2, 3))
    assert A == SDM({0:{0:ZZ(1)}, 1:{1:ZZ(2)}}, (2, 3), ZZ)

