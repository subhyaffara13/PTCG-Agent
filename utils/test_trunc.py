
def test_trunc():
    f, g = x**5 + 2*x**4 + 3*x**3 + 4*x**2 + 5*x + 6, x**5 - x**4 + x**2 - x
    F, G = Poly(f), Poly(g)

    assert F.trunc(3) == G
    assert trunc(f, 3) == g
    assert trunc(f, 3, x) == g
    assert trunc(f, 3, (x,)) == g
    assert trunc(F, 3) == G
    assert trunc(f, 3, polys=True) == G
    assert trunc(F, 3, polys=False) == g

    f, g = 6*x**5 + 5*x**4 + 4*x**3 + 3*x**2 + 2*x + 1, -x**4 + x**3 - x + 1
    F, G = Poly(f), Poly(g)

    assert F.trunc(3) == G
    assert trunc(f, 3) == g
    assert trunc(f, 3, x) == g
    assert trunc(f, 3, (x,)) == g
    assert trunc(F, 3) == G
    assert trunc(f, 3, polys=True) == G
    assert trunc(F, 3, polys=False) == g

    f = Poly(x**2 + 2*x + 3, modulus=5)

    assert f.trunc(2) == Poly(x**2 + 1, modulus=5)


def test_trunc():
    R, x, y, t = ring('x, y, t', QQ)
    p = (y + t*x)**4
    p1 = rs_trunc(p, x, 3)
    assert p1 == y**4 + 4*y**3*t*x + 6*y**2*t**2*x**2


def test_trunc():
    import math
    x, y = symbols('x y')
    assert math.trunc(2) == 2
    assert math.trunc(4.57) == 4
    assert math.trunc(-5.79) == -5
    assert math.trunc(pi) == 3
    assert math.trunc(log(7)) == 1
    assert math.trunc(exp(5)) == 148
    assert math.trunc(cos(pi)) == -1
    assert math.trunc(sin(5)) == 0

    raises(TypeError, lambda: math.trunc(x))
    raises(TypeError, lambda: math.trunc(x + y**2))
    raises(TypeError, lambda: math.trunc(oo))

