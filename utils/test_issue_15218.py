
def test_issue_15218():
    with warns_deprecated_sympy():
        Integral(Eq(x, y))
    with warns_deprecated_sympy():
        assert Integral(Eq(x, y), x) == Eq(Integral(x, x), Integral(y, x))
    with warns_deprecated_sympy():
        assert Integral(Eq(x, y), x).doit() == Eq(x**2/2, x*y)
    with warns(SymPyDeprecationWarning, test_stacklevel=False):
        # The warning is made in the ExprWithLimits superclass. The stacklevel
        # is correct for integrate(Eq) but not Eq.integrate
        assert Eq(x, y).integrate(x) == Eq(x**2/2, x*y)

    # These are not deprecated because they are definite integrals
    assert integrate(Eq(x, y), (x, 0, 1)) == Eq(S.Half, y)
    assert Eq(x, y).integrate((x, 0, 1)) == Eq(S.Half, y)

