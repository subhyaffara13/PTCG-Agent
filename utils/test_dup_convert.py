
def test_dup_convert():
    K0, K1 = ZZ['x'], ZZ

    f = [K0(1), K0(2), K0(0), K0(3)]

    assert dup_convert(f, K0, K1) == \
        [ZZ(1), ZZ(2), ZZ(0), ZZ(3)]

