
def test_Domain__algebraic_field():
    alg = ZZ.algebraic_field(sqrt(2))
    assert alg.ext.minpoly == Poly(x**2 - 2)
    assert alg.dom == QQ

    alg = QQ.algebraic_field(sqrt(2))
    assert alg.ext.minpoly == Poly(x**2 - 2)
    assert alg.dom == QQ

    alg = alg.algebraic_field(sqrt(3))
    assert alg.ext.minpoly == Poly(x**4 - 10*x**2 + 1)
    assert alg.dom == QQ

