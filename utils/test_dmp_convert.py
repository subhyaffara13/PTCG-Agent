
def test_dmp_convert():
    K0, K1 = ZZ['x'], ZZ

    f = [[K0(1)], [K0(2)], [], [K0(3)]]

    assert dmp_convert(f, 1, K0, K1) == \
        [[ZZ(1)], [ZZ(2)], [], [ZZ(3)]]

