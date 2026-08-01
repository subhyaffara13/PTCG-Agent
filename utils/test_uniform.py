
def test_uniform():
    l = Symbol('l', real=True)
    w = Symbol('w', positive=True)
    X = Uniform('x', l, l + w)

    assert E(X) == l + w/2
    assert variance(X).expand() == w**2/12

    # With numbers all is well
    X = Uniform('x', 3, 5)
    assert P(X < 3) == 0 and P(X > 5) == 0
    assert P(X < 4) == P(X > 4) == S.Half
    assert median(X) == FiniteSet(4)

    z = Symbol('z')
    p = density(X)(z)
    assert p.subs(z, 3.7) == S.Half
    assert p.subs(z, -1) == 0
    assert p.subs(z, 6) == 0

    c = cdf(X)
    assert c(2) == 0 and c(3) == 0
    assert c(Rational(7, 2)) == Rational(1, 4)
    assert c(5) == 1 and c(6) == 1

