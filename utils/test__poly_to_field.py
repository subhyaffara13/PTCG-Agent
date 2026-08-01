
def test_Poly_to_field():
    assert Poly(2*x + 1, domain='ZZ').to_field() == Poly(2*x + 1, domain='QQ')
    assert Poly(2*x + 1, domain='QQ').to_field() == Poly(2*x + 1, domain='QQ')

    assert Poly(x/2 + 1, domain='QQ').to_field() == Poly(x/2 + 1, domain='QQ')
    assert Poly(2*x + 1, modulus=3).to_field() == Poly(2*x + 1, modulus=3)

    assert Poly(2.0*x + 1.0).to_field() == Poly(2.0*x + 1.0)

