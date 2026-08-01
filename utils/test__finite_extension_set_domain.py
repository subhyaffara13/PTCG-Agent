
def test_FiniteExtension_set_domain():
    KZ = FiniteExtension(Poly(x**2 + 1, x, domain='ZZ'))
    KQ = FiniteExtension(Poly(x**2 + 1, x, domain='QQ'))
    assert KZ.set_domain(QQ) == KQ

