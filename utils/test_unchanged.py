
def test_unchanged():
    assert unchanged(MatPow, C, 0)
    assert unchanged(MatPow, C, 1)
    assert unchanged(MatPow, Inverse(C), -1)
    assert unchanged(Inverse, MatPow(C, -1), -1)
    assert unchanged(MatPow, MatPow(C, -1), -1)
    assert unchanged(MatPow, MatPow(C, 1), 1)

