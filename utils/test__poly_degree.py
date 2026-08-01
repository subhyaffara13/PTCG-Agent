
def test_Poly_degree():
    assert Poly(0, x).degree() is -oo
    assert Poly(1, x).degree() == 0
    assert Poly(x, x).degree() == 1

    assert Poly(0, x).degree(gen=0) is -oo
    assert Poly(1, x).degree(gen=0) == 0
    assert Poly(x, x).degree(gen=0) == 1

    assert Poly(0, x).degree(gen=x) is -oo
    assert Poly(1, x).degree(gen=x) == 0
    assert Poly(x, x).degree(gen=x) == 1

    assert Poly(0, x).degree(gen='x') is -oo
    assert Poly(1, x).degree(gen='x') == 0
    assert Poly(x, x).degree(gen='x') == 1

    raises(PolynomialError, lambda: Poly(1, x).degree(gen=1))
    raises(PolynomialError, lambda: Poly(1, x).degree(gen=y))
    raises(PolynomialError, lambda: Poly(1, x).degree(gen='y'))

    assert Poly(1, x, y).degree() == 0
    assert Poly(2*y, x, y).degree() == 0
    assert Poly(x*y, x, y).degree() == 1

    assert Poly(1, x, y).degree(gen=x) == 0
    assert Poly(2*y, x, y).degree(gen=x) == 0
    assert Poly(x*y, x, y).degree(gen=x) == 1

    assert Poly(1, x, y).degree(gen=y) == 0
    assert Poly(2*y, x, y).degree(gen=y) == 1
    assert Poly(x*y, x, y).degree(gen=y) == 1

    assert degree(0, x) is -oo
    assert degree(1, x) == 0
    assert degree(x, x) == 1

    assert degree(x*y**2, x) == 1
    assert degree(x*y**2, y) == 2
    assert degree(x*y**2, z) == 0

    assert degree(pi) == 1

    raises(TypeError, lambda: degree(y**2 + x**3))
    raises(TypeError, lambda: degree(y**2 + x**3, 1))
    raises(PolynomialError, lambda: degree(x, 1.1))
    raises(PolynomialError, lambda: degree(x**2/(x**3 + 1), x))

    assert degree(Poly(0,x),z) is -oo
    assert degree(Poly(1,x),z) == 0
    assert degree(Poly(x**2+y**3,y)) == 3
    assert degree(Poly(y**2 + x**3, y, x), 1) == 3
    assert degree(Poly(y**2 + x**3, x), z) == 0
    assert degree(Poly(y**2 + x**3 + z**4, x), z) == 4

