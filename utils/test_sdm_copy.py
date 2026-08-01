
def test_SDM_copy():
    A = SDM({0:{0:ZZ(1)}}, (2, 2), ZZ)
    B = A.copy()
    assert A == B
    A[0][0] = ZZ(2)
    assert A != B

