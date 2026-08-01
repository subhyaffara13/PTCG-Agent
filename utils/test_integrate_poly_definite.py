
def test_integrate_poly_definite():
    p = Poly(x + x**2*y + y**3, x, y)

    with warns_deprecated_sympy():
        Qx = Integral(p, (x, 0, 1))
    with warns(SymPyDeprecationWarning, test_stacklevel=False):
        Qx = integrate(p, (x, 0, 1))
    with warns(SymPyDeprecationWarning, test_stacklevel=False):
        Qy = integrate(p, (y, 0, pi))

    assert isinstance(Qx, Poly) is True
    assert isinstance(Qy, Poly) is True

    assert Qx.gens == (y,)
    assert Qy.gens == (x,)

    assert Qx.as_expr() == S.Half + y/3 + y**3
    assert Qy.as_expr() == pi**4/4 + pi*x + pi**2*x**2/2

