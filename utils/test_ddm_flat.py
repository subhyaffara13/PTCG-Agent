
def test_DDM_flat():
    dm = DDM([
        [ZZ(6), ZZ(4)],
        [ZZ(3), ZZ(1)]], (2, 2), ZZ)
    assert dm.flat() == [ZZ(6), ZZ(4), ZZ(3), ZZ(1)]

