
def test_Domain_cyclotomic_field():
    K = ZZ.cyclotomic_field(12)
    assert K.ext.minpoly == Poly(cyclotomic_poly(12))
    assert K.dom == QQ

    F = QQ.cyclotomic_field(3)
    assert F.ext.minpoly == Poly(cyclotomic_poly(3))
    assert F.dom == QQ

    E = F.cyclotomic_field(4)
    assert field_isomorphism(E.ext, K.ext) is not None
    assert E.dom == QQ

