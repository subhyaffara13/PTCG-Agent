
def test_all_roots():

    f = 2*x**3 - 7*x**2 + 4*x + 4
    froots = [Rational(-1, 2), 2, 2]
    assert all_roots(f) == Poly(f).all_roots() == froots

    g = x**3 + x + 1
    groots = [rootof(g, 0), rootof(g, 1), rootof(g, 2)]
    assert all_roots(g) == Poly(g).all_roots() == groots

    assert all_roots(x**2 - 2) == [-sqrt(2), sqrt(2)]
    assert all_roots(x**2 - 2, multiple=False) == [(-sqrt(2), 1), (sqrt(2), 1)]
    assert all_roots(x**2 - 2, radicals=False) == [
        rootof(x**2 - 2, 0, radicals=False),
        rootof(x**2 - 2, 1, radicals=False),
    ]

    p = x**5 - x - 1
    assert all_roots(p) == [
        rootof(p, 0), rootof(p, 1), rootof(p, 2), rootof(p, 3), rootof(p, 4)
    ]

    # testing extension
    f = x**2 + sqrt(2)
    roots = [-2**(S(1)/4)*I, 2**(S(1)/4)*I]
    raises(NotImplementedError, lambda: all_roots(f))
    raises(NotImplementedError, lambda : all_roots(Poly(f, x)))
    assert all_roots(f, extension=True) == roots
    assert all_roots(Poly(f, extension=True)) == roots
    assert all_roots(Poly(f), extension=True) == roots

