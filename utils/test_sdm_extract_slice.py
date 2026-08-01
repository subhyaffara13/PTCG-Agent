
def test_SDM_extract_slice():
    A = SDM({0:{0:ZZ(1), 1:ZZ(2)}, 1:{0:ZZ(3), 1:ZZ(4)}}, (2, 2), ZZ)
    B = A.extract_slice(slice(1, 2), slice(1, 2))
    assert B == SDM({0:{0:ZZ(4)}}, (1, 1), ZZ)

