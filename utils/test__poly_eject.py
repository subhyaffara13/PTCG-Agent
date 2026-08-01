
def test_Poly_eject():
    f = Poly(x**2*y + x*y**3 + x*y + 1, x, y)

    assert f.eject(x) == Poly(x*y**3 + (x**2 + x)*y + 1, y, domain='ZZ[x]')
    assert f.eject(y) == Poly(y*x**2 + (y**3 + y)*x + 1, x, domain='ZZ[y]')

    ex = x + y + z + t + w
    g = Poly(ex, x, y, z, t, w)

    assert g.eject(x) == Poly(ex, y, z, t, w, domain='ZZ[x]')
    assert g.eject(x, y) == Poly(ex, z, t, w, domain='ZZ[x, y]')
    assert g.eject(x, y, z) == Poly(ex, t, w, domain='ZZ[x, y, z]')
    assert g.eject(w) == Poly(ex, x, y, z, t, domain='ZZ[w]')
    assert g.eject(t, w) == Poly(ex, x, y, z, domain='ZZ[t, w]')
    assert g.eject(z, t, w) == Poly(ex, x, y, domain='ZZ[z, t, w]')

    raises(DomainError, lambda: Poly(x*y, x, y, domain=ZZ[z]).eject(y))
    raises(NotImplementedError, lambda: Poly(x*y, x, y, z).eject(y))

