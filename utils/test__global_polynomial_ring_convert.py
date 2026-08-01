
def test_GlobalPolynomialRing_convert():
    K1 = QQ.old_poly_ring(x)
    K2 = QQ[x]
    assert K1.convert(x) == K1.convert(K2.convert(x), K2)
    assert K2.convert(x) == K2.convert(K1.convert(x), K1)

    K1 = QQ.old_poly_ring(x, y)
    K2 = QQ[x]
    assert K1.convert(x) == K1.convert(K2.convert(x), K2)
    #assert K2.convert(x) == K2.convert(K1.convert(x), K1)

    K1 = ZZ.old_poly_ring(x, y)
    K2 = QQ[x]
    assert K1.convert(x) == K1.convert(K2.convert(x), K2)

