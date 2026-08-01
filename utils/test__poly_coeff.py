
def test_Poly_coeff():
    assert Poly(0, x).coeff_monomial(1) == 0
    assert Poly(0, x).coeff_monomial(x) == 0

    assert Poly(1, x).coeff_monomial(1) == 1
    assert Poly(1, x).coeff_monomial(x) == 0

    assert Poly(x**8, x).coeff_monomial(1) == 0
    assert Poly(x**8, x).coeff_monomial(x**7) == 0
    assert Poly(x**8, x).coeff_monomial(x**8) == 1
    assert Poly(x**8, x).coeff_monomial(x**9) == 0

    assert Poly(3*x*y**2 + 1, x, y).coeff_monomial(1) == 1
    assert Poly(3*x*y**2 + 1, x, y).coeff_monomial(x*y**2) == 3

    p = Poly(24*x*y*exp(8) + 23*x, x, y)

    assert p.coeff_monomial(x) == 23
    assert p.coeff_monomial(y) == 0
    assert p.coeff_monomial(x*y) == 24*exp(8)

    assert p.as_expr().coeff(x) == 24*y*exp(8) + 23
    raises(NotImplementedError, lambda: p.coeff(x))

    raises(ValueError, lambda: Poly(x + 1).coeff_monomial(0))
    raises(ValueError, lambda: Poly(x + 1).coeff_monomial(3*x))
    raises(ValueError, lambda: Poly(x + 1).coeff_monomial(3*x*y))

