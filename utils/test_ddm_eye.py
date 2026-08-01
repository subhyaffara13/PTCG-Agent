
def test_DDM_eye():
    ddmz = DDM.eye(3, QQ)
    f = lambda i, j: QQ(1) if i == j else QQ(0)
    assert list(ddmz) == [[f(i, j) for i in range(3)] for j in range(3)]
    assert ddmz.shape == (3, 3)
    assert ddmz.domain == QQ

