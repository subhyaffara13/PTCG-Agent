
def test_poly_deprecated():
    p = Poly(2*x, x)
    assert p.integrate(x) == Poly(x**2, x, domain='QQ')
    # The stacklevel is based on Integral(Poly)
    with warns(SymPyDeprecationWarning, test_stacklevel=False):
        integrate(p, x)
    with warns(SymPyDeprecationWarning, test_stacklevel=False):
        Integral(p, (x,))

