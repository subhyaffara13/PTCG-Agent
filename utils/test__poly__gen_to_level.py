
def test_Poly__gen_to_level():
    assert Poly(1, x, y)._gen_to_level(-2) == 0
    assert Poly(1, x, y)._gen_to_level(-1) == 1
    assert Poly(1, x, y)._gen_to_level( 0) == 0
    assert Poly(1, x, y)._gen_to_level( 1) == 1

    raises(PolynomialError, lambda: Poly(1, x, y)._gen_to_level(-3))
    raises(PolynomialError, lambda: Poly(1, x, y)._gen_to_level( 2))

    assert Poly(1, x, y)._gen_to_level(x) == 0
    assert Poly(1, x, y)._gen_to_level(y) == 1

    assert Poly(1, x, y)._gen_to_level('x') == 0
    assert Poly(1, x, y)._gen_to_level('y') == 1

    raises(PolynomialError, lambda: Poly(1, x, y)._gen_to_level(z))
    raises(PolynomialError, lambda: Poly(1, x, y)._gen_to_level('z'))

