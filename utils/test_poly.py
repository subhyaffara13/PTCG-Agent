
def test_poly():
    assert poly(x) == Poly(x, x)
    assert poly(y) == Poly(y, y)

    assert poly(x + y) == Poly(x + y, x, y)
    assert poly(x + sin(x)) == Poly(x + sin(x), x, sin(x))

    assert poly(x + y, wrt=y) == Poly(x + y, y, x)
    assert poly(x + sin(x), wrt=sin(x)) == Poly(x + sin(x), sin(x), x)

    assert poly(x*y + 2*x*z**2 + 17) == Poly(x*y + 2*x*z**2 + 17, x, y, z)

    assert poly(2*(y + z)**2 - 1) == Poly(2*y**2 + 4*y*z + 2*z**2 - 1, y, z)
    assert poly(
        x*(y + z)**2 - 1) == Poly(x*y**2 + 2*x*y*z + x*z**2 - 1, x, y, z)
    assert poly(2*x*(
        y + z)**2 - 1) == Poly(2*x*y**2 + 4*x*y*z + 2*x*z**2 - 1, x, y, z)

    assert poly(2*(
        y + z)**2 - x - 1) == Poly(2*y**2 + 4*y*z + 2*z**2 - x - 1, x, y, z)
    assert poly(x*(
        y + z)**2 - x - 1) == Poly(x*y**2 + 2*x*y*z + x*z**2 - x - 1, x, y, z)
    assert poly(2*x*(y + z)**2 - x - 1) == Poly(2*x*y**2 + 4*x*y*z + 2*
                x*z**2 - x - 1, x, y, z)

    assert poly(x*y + (x + y)**2 + (x + z)**2) == \
        Poly(2*x*z + 3*x*y + y**2 + z**2 + 2*x**2, x, y, z)
    assert poly(x*y*(x + y)*(x + z)**2) == \
        Poly(x**3*y**2 + x*y**2*z**2 + y*x**2*z**2 + 2*z*x**2*
             y**2 + 2*y*z*x**3 + y*x**4, x, y, z)

    assert poly(Poly(x + y + z, y, x, z)) == Poly(x + y + z, y, x, z)

    assert poly((x + y)**2, x) == Poly(x**2 + 2*x*y + y**2, x, domain=ZZ[y])
    assert poly((x + y)**2, y) == Poly(x**2 + 2*x*y + y**2, y, domain=ZZ[x])

    assert poly(1, x) == Poly(1, x)
    raises(GeneratorsNeeded, lambda: poly(1))

    # issue 6184
    assert poly(x + y, x, y) == Poly(x + y, x, y)
    assert poly(x + y, y, x) == Poly(x + y, y, x)

    # https://github.com/sympy/sympy/issues/19755
    expr1 = x + (2*x + 3)**2/5 + S(6)/5
    assert poly(expr1).as_expr() == expr1.expand()
    expr2 = y*(y+1) + S(1)/3
    assert poly(expr2).as_expr() == expr2.expand()

