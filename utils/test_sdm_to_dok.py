
def test_SDM_to_dok():
    A = SDM({0:{1: ZZ(1)}}, (2, 2), ZZ)
    assert A.to_dok() == {(0, 1): ZZ(1)}

