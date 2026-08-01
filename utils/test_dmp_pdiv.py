
def test_dmp_pdiv():
    f = dmp_normal([[1], [], [1, 0, 0]], 1, ZZ)
    g = dmp_normal([[1], [-1, 0]], 1, ZZ)

    q = dmp_normal([[1], [1, 0]], 1, ZZ)
    r = dmp_normal([[2, 0, 0]], 1, ZZ)

    assert dmp_pdiv(f, g, 1, ZZ) == (q, r)
    assert dmp_pquo(f, g, 1, ZZ) == q
    assert dmp_prem(f, g, 1, ZZ) == r

    raises(ExactQuotientFailed, lambda: dmp_pexquo(f, g, 1, ZZ))

    f = dmp_normal([[1], [], [1, 0, 0]], 1, ZZ)
    g = dmp_normal([[2], [-2, 0]], 1, ZZ)

    q = dmp_normal([[2], [2, 0]], 1, ZZ)
    r = dmp_normal([[8, 0, 0]], 1, ZZ)

    assert dmp_pdiv(f, g, 1, ZZ) == (q, r)
    assert dmp_pquo(f, g, 1, ZZ) == q
    assert dmp_prem(f, g, 1, ZZ) == r

    raises(ExactQuotientFailed, lambda: dmp_pexquo(f, g, 1, ZZ))

