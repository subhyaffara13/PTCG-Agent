
def test_dmp_copy():
    f = [[ZZ(1)], [ZZ(2), ZZ(0)]]
    g = dmp_copy(f, 1)

    g[0][0], g[1][1] = ZZ(7), ZZ(1)

    assert f != g

