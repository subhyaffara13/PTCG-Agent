
def test_dmp_rr_div():
    raises(ZeroDivisionError, lambda: dmp_rr_div([[1, 2], [3]], [[]], 1, ZZ))

    f = dmp_normal([[1], [], [1, 0, 0]], 1, ZZ)
    g = dmp_normal([[1], [-1, 0]], 1, ZZ)

    q = dmp_normal([[1], [1, 0]], 1, ZZ)
    r = dmp_normal([[2, 0, 0]], 1, ZZ)

    assert dmp_rr_div(f, g, 1, ZZ) == (q, r)

    f = dmp_normal([[1], [], [1, 0, 0]], 1, ZZ)
    g = dmp_normal([[-1], [1, 0]], 1, ZZ)

    q = dmp_normal([[-1], [-1, 0]], 1, ZZ)
    r = dmp_normal([[2, 0, 0]], 1, ZZ)

    assert dmp_rr_div(f, g, 1, ZZ) == (q, r)

    f = dmp_normal([[1], [], [1, 0, 0]], 1, ZZ)
    g = dmp_normal([[2], [-2, 0]], 1, ZZ)

    q, r = [[]], f

    assert dmp_rr_div(f, g, 1, ZZ) == (q, r)

