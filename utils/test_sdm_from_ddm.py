
def test_SDM_from_ddm():
    A = DDM([[ZZ(1), ZZ(0)], [ZZ(1), ZZ(0)]], (2, 2), ZZ)
    B = SDM.from_ddm(A)
    assert B.domain == ZZ
    assert B.shape == (2, 2)
    assert dict(B) == {0:{0:ZZ(1)}, 1:{0:ZZ(1)}}

