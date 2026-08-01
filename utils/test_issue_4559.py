
def test_issue_4559():
    x = Symbol('x')
    e = Symbol('e')
    w = Wild('w', exclude=[x])
    y = Wild('y')

    # this is as it should be

    assert (3/x).match(w/y) == {w: 3, y: x}
    assert (3*x).match(w*y) == {w: 3, y: x}
    assert (x/3).match(y/w) == {w: 3, y: x}
    assert (3*x).match(y/w) == {w: S.One/3, y: x}
    assert (3*x).match(y/w) == {w: Rational(1, 3), y: x}

    # these could be allowed to fail

    assert (x/3).match(w/y) == {w: S.One/3, y: 1/x}
    assert (3*x).match(w/y) == {w: 3, y: 1/x}
    assert (3/x).match(w*y) == {w: 3, y: 1/x}

    # Note that solve will give
    # multiple roots but match only gives one:
    #
    # >>> solve(x**r-y**2,y)
    # [-x**(r/2), x**(r/2)]

    r = Symbol('r', rational=True)
    assert (x**r).match(y**2) == {y: x**(r/2)}
    assert (x**e).match(y**2) == {y: sqrt(x**e)}

    # since (x**i = y) -> x = y**(1/i) where i is an integer
    # the following should also be valid as long as y is not
    # zero when i is negative.

    a = Wild('a')

    e = S.Zero
    assert e.match(a) == {a: e}
    assert e.match(1/a) is None
    assert e.match(a**.3) is None

    e = S(3)
    assert e.match(1/a) == {a: 1/e}
    assert e.match(1/a**2) == {a: 1/sqrt(e)}
    e = pi
    assert e.match(1/a) == {a: 1/e}
    assert e.match(1/a**2) == {a: 1/sqrt(e)}
    assert (-e).match(sqrt(a)) is None
    assert (-e).match(a**2) == {a: I*sqrt(pi)}

