
def test_Poly_set_domain():
    assert Poly(2*x + 1).set_domain(ZZ) == Poly(2*x + 1)
    assert Poly(2*x + 1).set_domain('ZZ') == Poly(2*x + 1)

    assert Poly(2*x + 1).set_domain(QQ) == Poly(2*x + 1, domain='QQ')
    assert Poly(2*x + 1).set_domain('QQ') == Poly(2*x + 1, domain='QQ')

    assert Poly(Rational(2, 10)*x + Rational(1, 10)).set_domain('RR') == Poly(0.2*x + 0.1)
    assert Poly(0.2*x + 0.1).set_domain('QQ') == Poly(Rational(2, 10)*x + Rational(1, 10))

    raises(CoercionFailed, lambda: Poly(x/2 + 1).set_domain(ZZ))
    raises(CoercionFailed, lambda: Poly(x + 1, modulus=2).set_domain(QQ))

    raises(GeneratorsError, lambda: Poly(x*y, x, y).set_domain(ZZ[y]))

