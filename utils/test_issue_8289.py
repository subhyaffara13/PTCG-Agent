
def test_issue_8289():
    roots = (Poly(x**2 + 2)*Poly(x**4 + 2)).all_roots()
    assert _check(roots)
    roots = Poly(x**6 + 3*x**3 + 2, x).all_roots()
    assert _check(roots)
    roots = Poly(x**6 - x + 1).all_roots()
    assert _check(roots)
    # all imaginary roots with multiplicity of 2
    roots = Poly(x**4 + 4*x**2 + 4, x).all_roots()
    assert _check(roots)

