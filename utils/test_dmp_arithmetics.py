
def test_DMP_arithmetics():
    f = DMP([[ZZ(2)], [ZZ(2), ZZ(0)]], ZZ)

    assert f.mul_ground(2) == DMP([[ZZ(4)], [ZZ(4), ZZ(0)]], ZZ)
    assert f.quo_ground(2) == DMP([[ZZ(1)], [ZZ(1), ZZ(0)]], ZZ)

    raises(ExactQuotientFailed, lambda: f.exquo_ground(3))

    f = DMP([[ZZ(-5)]], ZZ)
    g = DMP([[ZZ(5)]], ZZ)

    assert f.abs() == g
    assert abs(f) == g

    assert g.neg() == f
    assert -g == f

    h = DMP([[]], ZZ)

    assert f.add(g) == h
    assert f + g == h
    assert g + f == h
    assert f + 5 == h
    assert 5 + f == h

    h = DMP([[ZZ(-10)]], ZZ)

    assert f.sub(g) == h
    assert f - g == h
    assert g - f == -h
    assert f - 5 == h
    assert 5 - f == -h

    h = DMP([[ZZ(-25)]], ZZ)

    assert f.mul(g) == h
    assert f * g == h
    assert g * f == h
    assert f * 5 == h
    assert 5 * f == h

    h = DMP([[ZZ(25)]], ZZ)

    assert f.sqr() == h
    assert f.pow(2) == h
    assert f**2 == h

    raises(TypeError, lambda: f.pow('x'))

    f = DMP([[ZZ(1)], [], [ZZ(1), ZZ(0), ZZ(0)]], ZZ)
    g = DMP([[ZZ(2)], [ZZ(-2), ZZ(0)]], ZZ)

    q = DMP([[ZZ(2)], [ZZ(2), ZZ(0)]], ZZ)
    r = DMP([[ZZ(8), ZZ(0), ZZ(0)]], ZZ)

    assert f.pdiv(g) == (q, r)
    assert f.pquo(g) == q
    assert f.prem(g) == r

    raises(ExactQuotientFailed, lambda: f.pexquo(g))

    f = DMP([[ZZ(1)], [], [ZZ(1), ZZ(0), ZZ(0)]], ZZ)
    g = DMP([[ZZ(1)], [ZZ(-1), ZZ(0)]], ZZ)

    q = DMP([[ZZ(1)], [ZZ(1), ZZ(0)]], ZZ)
    r = DMP([[ZZ(2), ZZ(0), ZZ(0)]], ZZ)

    assert f.div(g) == (q, r)
    assert f.quo(g) == q
    assert f.rem(g) == r

    assert divmod(f, g) == (q, r)
    assert f // g == q
    assert f % g == r

    raises(ExactQuotientFailed, lambda: f.exquo(g))

    f = DMP([ZZ(1), ZZ(0), ZZ(-1)], ZZ)
    g = DMP([ZZ(2), ZZ(-2)], ZZ)

    q = DMP([], ZZ)
    r = f

    pq = DMP([ZZ(2), ZZ(2)], ZZ)
    pr = DMP([], ZZ)

    assert f.div(g) == (q, r)
    assert f.quo(g) == q
    assert f.rem(g) == r

    assert divmod(f, g) == (q, r)
    assert f // g == q
    assert f % g == r

    raises(ExactQuotientFailed, lambda: f.exquo(g))

    assert f.pdiv(g) == (pq, pr)
    assert f.pquo(g) == pq
    assert f.prem(g) == pr
    assert f.pexquo(g) == pq

