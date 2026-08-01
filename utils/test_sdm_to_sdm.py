
def test_SDM_to_sdm():
    A = SDM({0:{1: ZZ(1)}}, (2, 2), ZZ)
    assert A.to_sdm() == A

