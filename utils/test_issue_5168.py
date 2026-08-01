
def test_issue_5168():
    a, b, c = symbols('a b c', cls=Wild)
    x = Symbol('x')
    f = Function('f')

    assert x.match(a) == {a: x}
    assert x.match(a*f(x)**c) == {a: x, c: 0}
    assert x.match(a*b) == {a: 1, b: x}
    assert x.match(a*b*f(x)**c) == {a: 1, b: x, c: 0}

    assert (-x).match(a) == {a: -x}
    assert (-x).match(a*f(x)**c) == {a: -x, c: 0}
    assert (-x).match(a*b) == {a: -1, b: x}
    assert (-x).match(a*b*f(x)**c) == {a: -1, b: x, c: 0}

    assert (2*x).match(a) == {a: 2*x}
    assert (2*x).match(a*f(x)**c) == {a: 2*x, c: 0}
    assert (2*x).match(a*b) == {a: 2, b: x}
    assert (2*x).match(a*b*f(x)**c) == {a: 2, b: x, c: 0}

    assert (-2*x).match(a) == {a: -2*x}
    assert (-2*x).match(a*f(x)**c) == {a: -2*x, c: 0}
    assert (-2*x).match(a*b) == {a: -2, b: x}
    assert (-2*x).match(a*b*f(x)**c) == {a: -2, b: x, c: 0}

