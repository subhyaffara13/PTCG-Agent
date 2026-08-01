
def test_issue_19113():
    eq = cos(x)**3 - cos(x) + 1
    raises(PolynomialError, lambda: roots(eq))


def test_issue_19113():
    eq = sin(x)**3 - sin(x) + 1
    raises(PolynomialError, lambda: refine_root(eq, 1, 2, 1e-2))
    raises(PolynomialError, lambda: count_roots(eq, -1, 1))
    raises(PolynomialError, lambda: real_roots(eq))
    raises(PolynomialError, lambda: nroots(eq))
    raises(PolynomialError, lambda: ground_roots(eq))
    raises(PolynomialError, lambda: nth_power_roots_poly(eq, 2))


def test_issue_19113():
    eq = y**3 - y + 1
    # generator is a canonical x in RootOf
    assert str(Poly(eq).real_roots()) == '[CRootOf(x**3 - x + 1, 0)]'
    assert str(Poly(eq.subs(y, tan(y))).real_roots()
        ) == '[CRootOf(x**3 - x + 1, 0)]'
    assert str(Poly(eq.subs(y, tan(x))).real_roots()
        ) == '[CRootOf(x**3 - x + 1, 0)]'

