
def test_match_exclude():
    x = Symbol('x')
    y = Symbol('y')
    p = Wild("p")
    q = Wild("q")
    r = Wild("r")

    e = Rational(6)
    assert e.match(2*p) == {p: 3}

    e = 3/(4*x + 5)
    assert e.match(3/(p*x + q)) == {p: 4, q: 5}

    e = 3/(4*x + 5)
    assert e.match(p/(q*x + r)) == {p: 3, q: 4, r: 5}

    e = 2/(x + 1)
    assert e.match(p/(q*x + r)) == {p: 2, q: 1, r: 1}

    e = 1/(x + 1)
    assert e.match(p/(q*x + r)) == {p: 1, q: 1, r: 1}

    e = 4*x + 5
    assert e.match(p*x + q) == {p: 4, q: 5}

    e = 4*x + 5*y + 6
    assert e.match(p*x + q*y + r) == {p: 4, q: 5, r: 6}

    a = Wild('a', exclude=[x])

    e = 3*x
    assert e.match(p*x) == {p: 3}
    assert e.match(a*x) == {a: 3}

    e = 3*x**2
    assert e.match(p*x) == {p: 3*x}
    assert e.match(a*x) is None

    e = 3*x + 3 + 6/x
    assert e.match(p*x**2 + p*x + 2*p) == {p: 3/x}
    assert e.match(a*x**2 + a*x + 2*a) is None

