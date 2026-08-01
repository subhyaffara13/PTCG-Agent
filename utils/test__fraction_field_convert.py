
def test_FractionField_convert():
    K = QQ.frac_field(x)
    assert K.convert(QQ(2, 3), QQ) == K.from_sympy(Rational(2, 3))
    K = QQ.frac_field(x)
    assert K.convert(ZZ(2), ZZ) == K.from_sympy(Integer(2))

