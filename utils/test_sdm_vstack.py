
def test_SDM_vstack():
    A = SDM({0:{1:ZZ(1)}}, (2, 2), ZZ)
    B = SDM({1:{1:ZZ(1)}}, (2, 2), ZZ)
    AA = SDM({0:{1:ZZ(1)}, 2:{1:ZZ(1)}}, (4, 2), ZZ)
    AB = SDM({0:{1:ZZ(1)}, 3:{1:ZZ(1)}}, (4, 2), ZZ)
    assert SDM.vstack(A) == A
    assert SDM.vstack(A, A) == AA
    assert SDM.vstack(A, B) == AB

