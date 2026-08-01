
def test_dup_copy():
    f = [ZZ(1), ZZ(0), ZZ(2)]
    g = dup_copy(f)

    g[0], g[2] = ZZ(7), ZZ(0)

    assert f != g

