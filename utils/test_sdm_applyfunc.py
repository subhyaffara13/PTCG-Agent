
def test_SDM_applyfunc():
    A = SDM({0:{1:ZZ(1)}}, (2, 2), ZZ)
    B = SDM({0:{1:ZZ(2)}}, (2, 2), ZZ)
    assert A.applyfunc(lambda x: 2*x, ZZ) == B

