
def test_issue_8285():
    roots = (Poly(4*x**8 - 1, x)*Poly(x**2 + 1)).all_roots()
    assert _check(roots)
    f = Poly(x**4 + 5*x**2 + 6, x)
    ro = [rootof(f, i) for i in range(4)]
    roots = Poly(x**4 + 5*x**2 + 6, x).all_roots()
    assert roots == ro
    assert _check(roots)
    # more than 2 complex roots from which to identify the
    # imaginary ones
    roots = Poly(2*x**8 - 1).all_roots()
    assert _check(roots)
    assert len(Poly(2*x**10 - 1).all_roots()) == 10  # doesn't fail

