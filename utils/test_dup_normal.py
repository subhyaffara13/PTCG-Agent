
def test_dup_normal():
    assert dup_normal([0, 0, 2, 1, 0, 11, 0], ZZ) == \
        [ZZ(2), ZZ(1), ZZ(0), ZZ(11), ZZ(0)]

