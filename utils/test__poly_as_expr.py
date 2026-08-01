
def test_Poly_as_expr():
    assert Poly(0, x).as_expr() == 0
    assert Poly(0, x, y, z).as_expr() == 0

    assert Poly(1, x).as_expr() == 1
    assert Poly(1, x, y, z).as_expr() == 1

    assert Poly(x**2 + 3, x).as_expr() == x**2 + 3
    assert Poly(x**2 + 3, x, y, z).as_expr() == x**2 + 3

    assert Poly(
        3*x**2*y*z**3 + 4*x*y + 5*x*z).as_expr() == 3*x**2*y*z**3 + 4*x*y + 5*x*z

    f = Poly(x**2 + 2*x*y**2 - y, x, y)

    assert f.as_expr() == -y + x**2 + 2*x*y**2

    assert f.as_expr({x: 5}) == 25 - y + 10*y**2
    assert f.as_expr({y: 6}) == -6 + 72*x + x**2

    assert f.as_expr({x: 5, y: 6}) == 379
    assert f.as_expr(5, 6) == 379

    raises(GeneratorsError, lambda: f.as_expr({z: 7}))

