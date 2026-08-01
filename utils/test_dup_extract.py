
def test_dup_extract():
    f = dup_normal([2930944, 0, 2198208, 0, 549552, 0, 45796], ZZ)
    g = dup_normal([17585664, 0, 8792832, 0, 1099104, 0], ZZ)

    F = dup_normal([64, 0, 48, 0, 12, 0, 1], ZZ)
    G = dup_normal([384, 0, 192, 0, 24, 0], ZZ)

    assert dup_extract(f, g, ZZ) == (45796, F, G)

