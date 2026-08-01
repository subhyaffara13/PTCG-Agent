
def test_make_monic_over_integers_by_scaling_roots():
    f = Poly(x**2 + 3*x + 4, x, domain='ZZ')
    g, c = f.make_monic_over_integers_by_scaling_roots()
    assert g == f
    assert c == ZZ.one

    f = Poly(x**2 + 3*x + 4, x, domain='QQ')
    g, c = f.make_monic_over_integers_by_scaling_roots()
    assert g == f.to_ring()
    assert c == ZZ.one

    f = Poly(x**2/2 + S(1)/4 * x + S(1)/8, x, domain='QQ')
    g, c = f.make_monic_over_integers_by_scaling_roots()
    assert g == Poly(x**2 + 2*x + 4, x, domain='ZZ')
    assert c == 4

    f = Poly(x**3/2 + S(1)/4 * x + S(1)/8, x, domain='QQ')
    g, c = f.make_monic_over_integers_by_scaling_roots()
    assert g == Poly(x**3 + 8*x + 16, x, domain='ZZ')
    assert c == 4

    f = Poly(x*y, x, y)
    raises(ValueError, lambda: f.make_monic_over_integers_by_scaling_roots())

    f = Poly(x, domain='RR')
    raises(ValueError, lambda: f.make_monic_over_integers_by_scaling_roots())

