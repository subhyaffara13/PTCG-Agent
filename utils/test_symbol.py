
def test_symbol():
    x = Symbol('x')
    a, b, c, p, q = map(Wild, 'abcpq')

    e = x
    assert e.match(x) == {}
    assert e.matches(x) == {}
    assert e.match(a) == {a: x}

    e = Rational(5)
    assert e.match(c) == {c: 5}
    assert e.match(e) == {}
    assert e.match(e + 1) is None


def test_symbol(poly, tgt):
    p = poly([1, 2, 3], symbol='z')
    assert_equal(f"{p:unicode}", tgt)

