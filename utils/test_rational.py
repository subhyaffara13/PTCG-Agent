
def test_rational():
    assert limit(1/y - (1/(y + x) + x/(y + x)/y)/z, x, oo) == (z - 1)/(y*z)
    assert limit(1/y - (1/(y + x) + x/(y + x)/y)/z, x, -oo) == (z - 1)/(y*z)


def test_rational():
    a = Rational(1, 5)

    r = sqrt(5)/5
    assert sqrt(a) == r
    assert 2*sqrt(a) == 2*r

    r = a*a**S.Half
    assert a**Rational(3, 2) == r
    assert 2*a**Rational(3, 2) == 2*r

    r = a**5*a**Rational(2, 3)
    assert a**Rational(17, 3) == r
    assert 2 * a**Rational(17, 3) == 2*r


def test_rational():
    assert ask(Q.rational(x), Q.integer(x)) is True
    assert ask(Q.rational(x), Q.irrational(x)) is False
    assert ask(Q.rational(x), Q.real(x)) is None
    assert ask(Q.rational(x), Q.positive(x)) is None
    assert ask(Q.rational(x), Q.negative(x)) is None
    assert ask(Q.rational(x), Q.nonzero(x)) is None
    assert ask(Q.rational(x), ~Q.algebraic(x)) is False

    assert ask(Q.rational(2*x), Q.rational(x)) is True
    assert ask(Q.rational(2*x), Q.integer(x)) is True
    assert ask(Q.rational(2*x), Q.even(x)) is True
    assert ask(Q.rational(2*x), Q.odd(x)) is True
    assert ask(Q.rational(2*x), Q.irrational(x)) is False

    assert ask(Q.rational(x/2), Q.rational(x)) is True
    assert ask(Q.rational(x/2), Q.integer(x)) is True
    assert ask(Q.rational(x/2), Q.even(x)) is True
    assert ask(Q.rational(x/2), Q.odd(x)) is True
    assert ask(Q.rational(x/2), Q.irrational(x)) is False

    assert ask(Q.rational(1/x), Q.rational(x) & Q.nonzero(x)) is True
    assert ask(Q.rational(1/x), Q.integer(x) & Q.nonzero(x)) is True
    assert ask(Q.rational(1/x), Q.even(x) & Q.nonzero(x)) is True
    assert ask(Q.rational(1/x), Q.odd(x)) is True
    assert ask(Q.rational(1/x), Q.irrational(x)) is False

    assert ask(Q.rational(2/x), Q.rational(x) & Q.nonzero(x)) is True
    assert ask(Q.rational(2/x), Q.integer(x) & Q.nonzero(x)) is True
    assert ask(Q.rational(2/x), Q.even(x) & Q.nonzero(x)) is True
    assert ask(Q.rational(2/x), Q.odd(x)) is True
    assert ask(Q.rational(2/x), Q.irrational(x)) is False

    assert ask(Q.rational(x), ~Q.algebraic(x)) is False

    # with multiple symbols
    assert ask(Q.rational(x*y), Q.irrational(x) & Q.irrational(y)) is None
    assert ask(Q.rational(y/x), Q.rational(x) & Q.rational(y) & Q.nonzero(x)) is True
    assert ask(Q.rational(y/x), Q.integer(x) & Q.rational(y) & Q.nonzero(x)) is True
    assert ask(Q.rational(y/x), Q.even(x) & Q.rational(y) & Q.nonzero(x)) is True
    assert ask(Q.rational(y/x), Q.odd(x) & Q.rational(y)) is True
    assert ask(Q.rational(y/x), Q.irrational(x) & Q.rational(y) & Q.nonzero(y)) is False

    for f in [exp, sin, tan, asin, atan, cos]:
        assert ask(Q.rational(f(7))) is False
        assert ask(Q.rational(f(7, evaluate=False))) is False
        assert ask(Q.rational(f(0, evaluate=False))) is True
        assert ask(Q.rational(f(x)), Q.rational(x)) is None
        assert ask(Q.rational(f(x)), Q.rational(x) & Q.nonzero(x)) is False

    for g in [log, acos]:
        assert ask(Q.rational(g(7))) is False
        assert ask(Q.rational(g(7, evaluate=False))) is False
        assert ask(Q.rational(g(1, evaluate=False))) is True
        assert ask(Q.rational(g(x)), Q.rational(x)) is None
        assert ask(Q.rational(g(x)), Q.rational(x) & Q.nonzero(x - 1)) is False

    for h in [cot, acot]:
        assert ask(Q.rational(h(7))) is False
        assert ask(Q.rational(h(7, evaluate=False))) is False
        assert ask(Q.rational(h(x)), Q.rational(x)) is False

    # https://github.com/sympy/sympy/issues/27442
    assert ask(Q.rational(x**y),Q.irrational(x) & Q.rational(y)) is None
    assert ask(Q.rational(x**y),Q.integer(x) & Q.prime(x) & Q.rational(y)) is None
    assert ask(Q.rational(x**y),Q.integer(x) & Q.integer(y)) is None
    assert ask(Q.rational(x**y),Q.integer(x) & Q.eq(x,0) & Q.integer(y)) is None
    assert ask(Q.rational(x**y),Q.eq(x,1) & Q.rational(y)) is None
    assert ask(Q.rational(x**y),Q.eq(x,-1) & Q.rational(y)) is None
    assert ask(Q.rational(x**y), Q.prime(x) & Q.rational(y)) is None
    assert ask(Q.rational(x**y), ~Q.rational(x) & Q.integer(y) ) is None
    assert ask(Q.rational(Pow(-1, x, evaluate=False), Q.rational(x))) is None
    assert ask(Q.rational(x**y), Q.integer(y) & ~Q. algebraic(x)) is None
    assert ask(Q.rational(x**y), Q.integer(y) & ~Q. algebraic(x) & ~Q.zero(x)) is None
    assert ask(Q.rational(x**y), Q.integer(y) & ~Q.algebraic(x) & Q.complex(x) & ~Q.real(x)) is None
    assert ask(Q.rational(x**y), Q.integer(y) & ~Q.algebraic(x) & Q.complex(x)) is None

