
def test_Poly__eq__():
    assert (Poly(x, x) == Poly(x, x)) is True
    assert (Poly(x, x, domain=QQ) == Poly(x, x)) is False
    assert (Poly(x, x) == Poly(x, x, domain=QQ)) is False

    assert (Poly(x, x, domain=ZZ[a]) == Poly(x, x)) is False
    assert (Poly(x, x) == Poly(x, x, domain=ZZ[a])) is False

    assert (Poly(x*y, x, y) == Poly(x, x)) is False

    assert (Poly(x, x, y) == Poly(x, x)) is False
    assert (Poly(x, x) == Poly(x, x, y)) is False

    assert (Poly(x**2 + 1, x) == Poly(y**2 + 1, y)) is False
    assert (Poly(y**2 + 1, y) == Poly(x**2 + 1, x)) is False

    f = Poly(x, x, domain=ZZ)
    g = Poly(x, x, domain=QQ)

    assert f.eq(g) is False
    assert f.ne(g) is True

    assert f.eq(g, strict=True) is False
    assert f.ne(g, strict=True) is True

    t0 = Symbol('t0')

    f =  Poly((t0/2 + x**2)*t**2 - x**2*t, t, domain='QQ[x,t0]')
    g =  Poly((t0/2 + x**2)*t**2 - x**2*t, t, domain='ZZ(x,t0)')

    assert (f == g) is False

