
def test_Domain_alg_field_from_poly():
    f = Poly(x**2 - 2)
    g = Poly(x**2 - 3)
    h = Poly(x**4 - 10*x**2 + 1)

    alg = ZZ.alg_field_from_poly(f)
    assert alg.ext.minpoly == f
    assert alg.dom == QQ

    alg = QQ.alg_field_from_poly(f)
    assert alg.ext.minpoly == f
    assert alg.dom == QQ

    alg = alg.alg_field_from_poly(g)
    assert alg.ext.minpoly == h
    assert alg.dom == QQ

