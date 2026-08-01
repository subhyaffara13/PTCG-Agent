
def test_Poly_to_ring():
    assert Poly(2*x + 1, domain='ZZ').to_ring() == Poly(2*x + 1, domain='ZZ')
    assert Poly(2*x + 1, domain='QQ').to_ring() == Poly(2*x + 1, domain='ZZ')

    raises(CoercionFailed, lambda: Poly(x/2 + 1).to_ring())
    raises(DomainError, lambda: Poly(2*x + 1, modulus=3).to_ring())

