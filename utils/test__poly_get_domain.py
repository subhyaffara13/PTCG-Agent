
def test_Poly_get_domain():
    assert Poly(2*x).get_domain() == ZZ

    assert Poly(2*x, domain='ZZ').get_domain() == ZZ
    assert Poly(2*x, domain='QQ').get_domain() == QQ

    assert Poly(x/2).get_domain() == QQ

    raises(CoercionFailed, lambda: Poly(x/2, domain='ZZ'))
    assert Poly(x/2, domain='QQ').get_domain() == QQ

    assert isinstance(Poly(0.2*x).get_domain(), RealField)

