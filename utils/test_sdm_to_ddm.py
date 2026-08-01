
def test_SDM_to_ddm():
    A = SDM({0:{1: ZZ(1)}}, (2, 2), ZZ)
    B = DDM([[ZZ(0), ZZ(1)], [ZZ(0), ZZ(0)]], (2, 2), ZZ)
    assert A.to_ddm() == B

