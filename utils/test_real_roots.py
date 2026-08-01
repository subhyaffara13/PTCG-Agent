
def test_real_roots():
    # cf. issue 6650
    x = Symbol('x', real=True)
    assert len(solve(x**5 + x**3 + 1)) == 1


def test_real_roots():

    assert real_roots(x) == [0]
    assert real_roots(x, multiple=False) == [(0, 1)]

    assert real_roots(x**3) == [0, 0, 0]
    assert real_roots(x**3, multiple=False) == [(0, 3)]

    assert real_roots(x*(x**3 + x + 3)) == [rootof(x**3 + x + 3, 0), 0]
    assert real_roots(x*(x**3 + x + 3), multiple=False) == [(rootof(
        x**3 + x + 3, 0), 1), (0, 1)]

    assert real_roots(
        x**3*(x**3 + x + 3)) == [rootof(x**3 + x + 3, 0), 0, 0, 0]
    assert real_roots(x**3*(x**3 + x + 3), multiple=False) == [(rootof(
        x**3 + x + 3, 0), 1), (0, 3)]

    assert real_roots(x**2 - 2, radicals=False) == [
            rootof(x**2 - 2, 0, radicals=False),
            rootof(x**2 - 2, 1, radicals=False),
        ]

    f = 2*x**3 - 7*x**2 + 4*x + 4
    g = x**3 + x + 1

    assert Poly(f).real_roots() == [Rational(-1, 2), 2, 2]
    assert Poly(g).real_roots() == [rootof(g, 0)]

    # testing extension
    f = x**2 - sqrt(2)
    roots = [-2**(S(1)/4), 2**(S(1)/4)]
    raises(NotImplementedError, lambda: real_roots(f))
    raises(NotImplementedError, lambda: real_roots(Poly(f, x)))
    assert real_roots(f, extension=True) == roots
    assert real_roots(Poly(f, extension=True)) == roots
    assert real_roots(Poly(f), extension=True) == roots

