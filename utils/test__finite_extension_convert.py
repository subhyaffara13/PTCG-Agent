
def test_FiniteExtension_convert():
    # Test from_MonogenicFiniteExtension
    K1 = FiniteExtension(Poly(x**2 + 1))
    K2 = QQ[x]
    x1, x2 = K1(x), K2(x)
    assert K1.convert(x2) == x1
    assert K2.convert(x1) == x2

    K = FiniteExtension(Poly(x**2 - 1, domain=QQ))
    assert K.convert_from(QQ(1, 2), QQ) == K.one/2

