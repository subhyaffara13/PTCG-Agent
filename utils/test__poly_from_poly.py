
def test_Poly_from_poly():
    f = Poly(x + 7, x, domain=ZZ)
    g = Poly(x + 2, x, modulus=3)
    h = Poly(x + y, x, y, domain=ZZ)

    K = FF(3)

    assert Poly.from_poly(f) == f
    assert Poly.from_poly(f, domain=K).rep == DMP([K(1), K(1)], K)
    assert Poly.from_poly(f, domain=ZZ).rep == DMP([ZZ(1), ZZ(7)], ZZ)
    assert Poly.from_poly(f, domain=QQ).rep == DMP([QQ(1), QQ(7)], QQ)

    assert Poly.from_poly(f, gens=x) == f
    assert Poly.from_poly(f, gens=x, domain=K).rep == DMP([K(1), K(1)], K)
    assert Poly.from_poly(f, gens=x, domain=ZZ).rep == DMP([ZZ(1), ZZ(7)], ZZ)
    assert Poly.from_poly(f, gens=x, domain=QQ).rep == DMP([QQ(1), QQ(7)], QQ)

    assert Poly.from_poly(f, gens=y) == Poly(x + 7, y, domain='ZZ[x]')
    raises(CoercionFailed, lambda: Poly.from_poly(f, gens=y, domain=K))
    raises(CoercionFailed, lambda: Poly.from_poly(f, gens=y, domain=ZZ))
    raises(CoercionFailed, lambda: Poly.from_poly(f, gens=y, domain=QQ))

    assert Poly.from_poly(f, gens=(x, y)) == Poly(x + 7, x, y, domain='ZZ')
    assert Poly.from_poly(
        f, gens=(x, y), domain=ZZ) == Poly(x + 7, x, y, domain='ZZ')
    assert Poly.from_poly(
        f, gens=(x, y), domain=QQ) == Poly(x + 7, x, y, domain='QQ')
    assert Poly.from_poly(
        f, gens=(x, y), modulus=3) == Poly(x + 7, x, y, domain='FF(3)')

    K = FF(2)

    assert Poly.from_poly(g) == g
    assert Poly.from_poly(g, domain=ZZ).rep == DMP([ZZ(1), ZZ(-1)], ZZ)
    raises(CoercionFailed, lambda: Poly.from_poly(g, domain=QQ))
    assert Poly.from_poly(g, domain=K).rep == DMP([K(1), K(0)], K)

    assert Poly.from_poly(g, gens=x) == g
    assert Poly.from_poly(g, gens=x, domain=ZZ).rep == DMP([ZZ(1), ZZ(-1)], ZZ)
    raises(CoercionFailed, lambda: Poly.from_poly(g, gens=x, domain=QQ))
    assert Poly.from_poly(g, gens=x, domain=K).rep == DMP([K(1), K(0)], K)

    K = FF(3)

    assert Poly.from_poly(h) == h
    assert Poly.from_poly(
        h, domain=ZZ).rep == DMP([[ZZ(1)], [ZZ(1), ZZ(0)]], ZZ)
    assert Poly.from_poly(
        h, domain=QQ).rep == DMP([[QQ(1)], [QQ(1), QQ(0)]], QQ)
    assert Poly.from_poly(h, domain=K).rep == DMP([[K(1)], [K(1), K(0)]], K)

    assert Poly.from_poly(h, gens=x) == Poly(x + y, x, domain=ZZ[y])
    raises(CoercionFailed, lambda: Poly.from_poly(h, gens=x, domain=ZZ))
    assert Poly.from_poly(
        h, gens=x, domain=ZZ[y]) == Poly(x + y, x, domain=ZZ[y])
    raises(CoercionFailed, lambda: Poly.from_poly(h, gens=x, domain=QQ))
    assert Poly.from_poly(
        h, gens=x, domain=QQ[y]) == Poly(x + y, x, domain=QQ[y])
    raises(CoercionFailed, lambda: Poly.from_poly(h, gens=x, modulus=3))

    assert Poly.from_poly(h, gens=y) == Poly(x + y, y, domain=ZZ[x])
    raises(CoercionFailed, lambda: Poly.from_poly(h, gens=y, domain=ZZ))
    assert Poly.from_poly(
        h, gens=y, domain=ZZ[x]) == Poly(x + y, y, domain=ZZ[x])
    raises(CoercionFailed, lambda: Poly.from_poly(h, gens=y, domain=QQ))
    assert Poly.from_poly(
        h, gens=y, domain=QQ[x]) == Poly(x + y, y, domain=QQ[x])
    raises(CoercionFailed, lambda: Poly.from_poly(h, gens=y, modulus=3))

    assert Poly.from_poly(h, gens=(x, y)) == h
    assert Poly.from_poly(
        h, gens=(x, y), domain=ZZ).rep == DMP([[ZZ(1)], [ZZ(1), ZZ(0)]], ZZ)
    assert Poly.from_poly(
        h, gens=(x, y), domain=QQ).rep == DMP([[QQ(1)], [QQ(1), QQ(0)]], QQ)
    assert Poly.from_poly(
        h, gens=(x, y), domain=K).rep == DMP([[K(1)], [K(1), K(0)]], K)

    assert Poly.from_poly(
        h, gens=(y, x)).rep == DMP([[ZZ(1)], [ZZ(1), ZZ(0)]], ZZ)
    assert Poly.from_poly(
        h, gens=(y, x), domain=ZZ).rep == DMP([[ZZ(1)], [ZZ(1), ZZ(0)]], ZZ)
    assert Poly.from_poly(
        h, gens=(y, x), domain=QQ).rep == DMP([[QQ(1)], [QQ(1), QQ(0)]], QQ)
    assert Poly.from_poly(
        h, gens=(y, x), domain=K).rep == DMP([[K(1)], [K(1), K(0)]], K)

    assert Poly.from_poly(
        h, gens=(x, y), field=True).rep == DMP([[QQ(1)], [QQ(1), QQ(0)]], QQ)
    assert Poly.from_poly(
        h, gens=(x, y), field=True).rep == DMP([[QQ(1)], [QQ(1), QQ(0)]], QQ)

