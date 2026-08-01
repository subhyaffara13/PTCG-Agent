
def test_Or():
    N = Normal('N', 0, 1)
    assert simplify(P(Or(N > 2, N < 1))) == \
        -erf(sqrt(2))/2 - erfc(sqrt(2)/2)/2 + Rational(3, 2)
    assert P(Or(N < 0, N < 1)) == P(N < 1)
    assert P(Or(N > 0, N < 0)) == 1


def test_Or():
    X = Geometric('X', S.Half)
    assert P(Or(X < 3, X > 4)) == Rational(13, 16)
    assert P(Or(X > 2, X > 1)) == P(X > 1)
    assert P(Or(X >= 3, X < 3)) == 1


def test_Or():
    args = [(True, True), (True, False), (False, None)]
    assert Or(*args) == (True, True)
    args = [(None, None), (False, None), (False, False)]
    assert Or(*args) == (None, None)


def test_Or():
    assert Or() is false
    assert Or(A) == A
    assert Or(True) is true
    assert Or(False) is false
    assert Or(True, True) is true
    assert Or(True, False) is true
    assert Or(False, False) is false
    assert Or(True, A) is true
    assert Or(False, A) == A
    assert Or(True, False, False) is true
    assert Or(True, False, A) is true
    assert Or(False, False, A) == A
    assert Or(1, A) is true
    raises(TypeError, lambda: Or(2, A))
    assert Or(A < 1, A >= 1) is true
    e = A > 1
    assert Or(e, e.canonical) == e
    g, l, ge, le = A > B, B < A, A >= B, B <= A
    assert Or(g, l, ge, le) == Or(g, ge)

