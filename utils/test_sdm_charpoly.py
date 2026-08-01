
def test_SDM_charpoly():
    A = SDM({0:{0:ZZ(1), 1:ZZ(2)}, 1:{0:ZZ(3), 1:ZZ(4)}}, (2, 2), ZZ)
    assert A.charpoly() == [ZZ(1), ZZ(-5), ZZ(-2)]

