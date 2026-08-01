
def test_dmp_swap():
    f = dmp_normal([[1, 0, 0], [], [1, 0], [], [1]], 1, ZZ)
    g = dmp_normal([[1, 0, 0, 0, 0], [1, 0, 0], [1]], 1, ZZ)

    assert dmp_swap(f, 1, 1, 1, ZZ) == f

    assert dmp_swap(f, 0, 1, 1, ZZ) == g
    assert dmp_swap(g, 0, 1, 1, ZZ) == f

    raises(IndexError, lambda: dmp_swap(f, -1, -7, 1, ZZ))

