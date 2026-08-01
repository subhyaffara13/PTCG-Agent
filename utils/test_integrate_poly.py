
def test_integrate_poly():
    p = Poly(x + x**2*y + y**3, x, y)

    # The stacklevel is based on Integral(Poly)
    with warns_deprecated_sympy():
        qx = Integral(p, x)
    with warns(SymPyDeprecationWarning, test_stacklevel=False):
        qx = integrate(p, x)
    with warns(SymPyDeprecationWarning, test_stacklevel=False):
        qy = integrate(p, y)

    assert isinstance(qx, Poly) is True
    assert isinstance(qy, Poly) is True

    assert qx.gens == (x, y)
    assert qy.gens == (x, y)

    assert qx.as_expr() == x**2/2 + x**3*y/3 + x*y**3
    assert qy.as_expr() == x*y + x**2*y**2/2 + y**4/4

