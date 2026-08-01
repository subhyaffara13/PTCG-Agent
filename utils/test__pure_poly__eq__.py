
def test_PurePoly__eq__():
    assert (PurePoly(x, x) == PurePoly(x, x)) is True
    assert (PurePoly(x, x, domain=QQ) == PurePoly(x, x)) is True
    assert (PurePoly(x, x) == PurePoly(x, x, domain=QQ)) is True

    assert (PurePoly(x, x, domain=ZZ[a]) == PurePoly(x, x)) is True
    assert (PurePoly(x, x) == PurePoly(x, x, domain=ZZ[a])) is True

    assert (PurePoly(x*y, x, y) == PurePoly(x, x)) is False

    assert (PurePoly(x, x, y) == PurePoly(x, x)) is False
    assert (PurePoly(x, x) == PurePoly(x, x, y)) is False

    assert (PurePoly(x**2 + 1, x) == PurePoly(y**2 + 1, y)) is True
    assert (PurePoly(y**2 + 1, y) == PurePoly(x**2 + 1, x)) is True

    f = PurePoly(x, x, domain=ZZ)
    g = PurePoly(x, x, domain=QQ)

    assert f.eq(g) is True
    assert f.ne(g) is False

    assert f.eq(g, strict=True) is False
    assert f.ne(g, strict=True) is True

    f = PurePoly(x, x, domain=ZZ)
    g = PurePoly(y, y, domain=QQ)

    assert f.eq(g) is True
    assert f.ne(g) is False

    assert f.eq(g, strict=True) is False
    assert f.ne(g, strict=True) is True

