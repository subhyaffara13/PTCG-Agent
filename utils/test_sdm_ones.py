
def test_SDM_ones():
    A = SDM.ones((1, 2), QQ)
    assert A.domain == QQ
    assert A.shape == (1, 2)
    assert dict(A) == {0:{0:QQ(1), 1:QQ(1)}}

