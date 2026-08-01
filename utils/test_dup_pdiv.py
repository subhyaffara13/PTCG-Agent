
def test_dup_pdiv():
    f = dup_normal([3, 1, 1, 5], ZZ)
    g = dup_normal([5, -3, 1], ZZ)

    q = dup_normal([15, 14], ZZ)
    r = dup_normal([52, 111], ZZ)

    assert dup_pdiv(f, g, ZZ) == (q, r)
    assert dup_pquo(f, g, ZZ) == q
    assert dup_prem(f, g, ZZ) == r

    raises(ExactQuotientFailed, lambda: dup_pexquo(f, g, ZZ))

    f = dup_normal([3, 1, 1, 5], QQ)
    g = dup_normal([5, -3, 1], QQ)

    q = dup_normal([15, 14], QQ)
    r = dup_normal([52, 111], QQ)

    assert dup_pdiv(f, g, QQ) == (q, r)
    assert dup_pquo(f, g, QQ) == q
    assert dup_prem(f, g, QQ) == r

    raises(ExactQuotientFailed, lambda: dup_pexquo(f, g, QQ))

