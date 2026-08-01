
def test_SDM_to_list_flat():
    A = SDM({0:{1: ZZ(1)}}, (2, 2), ZZ)
    assert A.to_list_flat() == [ZZ(0), ZZ(1), ZZ(0), ZZ(0)]

