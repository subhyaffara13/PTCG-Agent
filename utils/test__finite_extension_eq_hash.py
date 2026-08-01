
def test_FiniteExtension_eq_hash():
    # Test eq and hash
    p1 = Poly(x**2 - 2, x, domain=ZZ)
    p2 = Poly(x**2 - 2, x, domain=QQ)
    K1 = FiniteExtension(p1)
    K2 = FiniteExtension(p2)
    assert K1 == FiniteExtension(Poly(x**2 - 2))
    assert K2 != FiniteExtension(Poly(x**2 - 2))
    assert len({K1, K2, FiniteExtension(p1)}) == 2

