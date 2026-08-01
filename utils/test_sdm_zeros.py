
def test_SDM_zeros():
    A = SDM.zeros((2, 2), ZZ)
    assert A.domain == ZZ
    assert A.shape == (2, 2)
    assert dict(A) == {}

