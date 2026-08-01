
def test_Poly_get_modulus():
    assert Poly(x**2 + 1, modulus=2).get_modulus() == 2
    raises(PolynomialError, lambda: Poly(x**2 + 1).get_modulus())

