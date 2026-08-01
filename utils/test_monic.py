
def test_monic():
    f, g = 2*x - 1, x - S.Half
    F, G = Poly(f, domain='QQ'), Poly(g)

    assert F.monic() == G
    assert monic(f) == g
    assert monic(f, x) == g
    assert monic(f, (x,)) == g
    assert monic(F) == G
    assert monic(f, polys=True) == G
    assert monic(F, polys=False) == g

    raises(ComputationFailed, lambda: monic(4))

    assert monic(2*x**2 + 6*x + 4, auto=False) == x**2 + 3*x + 2
    raises(ExactQuotientFailed, lambda: monic(2*x + 6*x + 1, auto=False))

    assert monic(2.0*x**2 + 6.0*x + 4.0) == 1.0*x**2 + 3.0*x + 2.0
    assert monic(2*x**2 + 3*x + 4, modulus=5) == x**2 - x + 2

