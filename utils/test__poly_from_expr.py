
def test_Poly_from_expr():
    raises(GeneratorsNeeded, lambda: Poly.from_expr(S.Zero))
    raises(GeneratorsNeeded, lambda: Poly.from_expr(S(7)))

    F3 = FF(3)

    assert Poly.from_expr(x + 5, domain=F3).rep == DMP([F3(1), F3(2)], F3)
    assert Poly.from_expr(y + 5, domain=F3).rep == DMP([F3(1), F3(2)], F3)

    assert Poly.from_expr(x + 5, x, domain=F3).rep == DMP([F3(1), F3(2)], F3)
    assert Poly.from_expr(y + 5, y, domain=F3).rep == DMP([F3(1), F3(2)], F3)

    assert Poly.from_expr(x + y, domain=F3).rep == DMP([[F3(1)], [F3(1), F3(0)]], F3)
    assert Poly.from_expr(x + y, x, y, domain=F3).rep == DMP([[F3(1)], [F3(1), F3(0)]], F3)

    assert Poly.from_expr(x + 5).rep == DMP([ZZ(1), ZZ(5)], ZZ)
    assert Poly.from_expr(y + 5).rep == DMP([ZZ(1), ZZ(5)], ZZ)

    assert Poly.from_expr(x + 5, x).rep == DMP([ZZ(1), ZZ(5)], ZZ)
    assert Poly.from_expr(y + 5, y).rep == DMP([ZZ(1), ZZ(5)], ZZ)

    assert Poly.from_expr(x + 5, domain=ZZ).rep == DMP([ZZ(1), ZZ(5)], ZZ)
    assert Poly.from_expr(y + 5, domain=ZZ).rep == DMP([ZZ(1), ZZ(5)], ZZ)

    assert Poly.from_expr(x + 5, x, domain=ZZ).rep == DMP([ZZ(1), ZZ(5)], ZZ)
    assert Poly.from_expr(y + 5, y, domain=ZZ).rep == DMP([ZZ(1), ZZ(5)], ZZ)

    assert Poly.from_expr(x + 5, x, y, domain=ZZ).rep == DMP([[ZZ(1)], [ZZ(5)]], ZZ)
    assert Poly.from_expr(y + 5, x, y, domain=ZZ).rep == DMP([[ZZ(1), ZZ(5)]], ZZ)

