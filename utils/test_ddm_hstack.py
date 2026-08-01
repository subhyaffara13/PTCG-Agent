
def test_DDM_hstack():
    A = DDM([[ZZ(1), ZZ(2), ZZ(3)]], (1, 3), ZZ)
    B = DDM([[ZZ(4), ZZ(5)]], (1, 2), ZZ)
    C = DDM([[ZZ(6)]], (1, 1), ZZ)

    Ah = A.hstack(B)
    assert Ah.shape == (1, 5)
    assert Ah.domain == ZZ
    assert Ah == DDM([[ZZ(1), ZZ(2), ZZ(3), ZZ(4), ZZ(5)]], (1, 5), ZZ)

    Ah = A.hstack(B, C)
    assert Ah.shape == (1, 6)
    assert Ah.domain == ZZ
    assert Ah == DDM([[ZZ(1), ZZ(2), ZZ(3), ZZ(4), ZZ(5), ZZ(6)]], (1, 6), ZZ)

