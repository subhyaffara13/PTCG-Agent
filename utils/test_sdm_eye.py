
def test_SDM_eye():
    A = SDM.eye((2, 2), ZZ)
    assert A.domain == ZZ
    assert A.shape == (2, 2)
    assert dict(A) == {0:{0:ZZ(1)}, 1:{1:ZZ(1)}}

