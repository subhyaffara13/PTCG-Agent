
def test_DDM_ones():
    ddmone = DDM.ones((2, 3), QQ)
    assert list(ddmone) == [[QQ(1)] * 3] * 2
    assert ddmone.shape == (2, 3)
    assert ddmone.domain == QQ

