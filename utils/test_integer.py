
def test_integer(value: t.Any) -> bool:
    """Return true if the object is an integer.

    .. versionadded:: 2.11
    """
    return isinstance(value, int) and value is not True and value is not False


def test_integer():
    assert ask(Q.integer(x)) is None
    assert ask(Q.integer(x), Q.integer(x)) is True
    assert ask(Q.integer(x), ~Q.integer(x)) is False
    assert ask(Q.integer(x), ~Q.real(x)) is False
    assert ask(Q.integer(x), ~Q.positive(x)) is None
    assert ask(Q.integer(x), Q.even(x) | Q.odd(x)) is True

    assert ask(Q.integer(2*x), Q.integer(x)) is True
    assert ask(Q.integer(2*x), Q.even(x)) is True
    assert ask(Q.integer(2*x), Q.prime(x)) is True
    assert ask(Q.integer(2*x), Q.rational(x)) is None
    assert ask(Q.integer(2*x), Q.real(x)) is None
    assert ask(Q.integer(sqrt(2)*x), Q.integer(x)) is False
    assert ask(Q.integer(sqrt(2)*x), Q.irrational(x)) is None

    assert ask(Q.integer(x/2), Q.odd(x)) is False
    assert ask(Q.integer(x/2), Q.even(x)) is True
    assert ask(Q.integer(x/3), Q.odd(x)) is None
    assert ask(Q.integer(x/3), Q.even(x)) is None

    # https://github.com/sympy/sympy/issues/7286
    assert ask(Q.integer(Abs(x)),Q.integer(x)) is True
    assert ask(Q.integer(Abs(-x)),Q.integer(x)) is True
    assert ask(Q.integer(Abs(x)), ~Q.integer(x)) is None
    assert ask(Q.integer(Abs(x)),Q.complex(x)) is None
    assert ask(Q.integer(Abs(x+I*y)),Q.real(x) & Q.real(y)) is None

    # https://github.com/sympy/sympy/issues/27739
    assert ask(Q.integer(x/y), Q.integer(x) & Q.integer(y)) is None
    assert ask(Q.integer(1/x), Q.integer(x)) is None
    assert ask(Q.integer(x**y), Q.integer(x) & Q.integer(y)) is None
    assert ask(Q.integer(sqrt(5))) is False
    assert ask(Q.integer(x**y), Q.nonzero(x) & Q.zero(y)) is True
    assert ask(Q.integer(x**y), Q.integer(x) & Q.integer(y) & Q.positive(y)) is True
    assert ask(Q.integer(-1**x), Q.integer(x)) is True
    assert ask(Q.integer(x**y), Q.integer(x) & Q.integer(y) & Q.positive(y)) is True
    assert ask(Q.integer(x**y), Q.zero(x) & Q.integer(y) & Q.positive(y)) is True
    assert ask(Q.integer(pi**x), Q.zero(x)) is True
    assert ask(Q.integer(x**y), Q.imaginary(x) & Q.zero(y)) is True


def test_integer():
    assert satask(Q.integer(1)) is True
    assert satask(Q.integer(S.Half)) is False

    assert satask(Q.integer(x + y), Q.integer(x) & Q.integer(y)) is True
    assert satask(Q.integer(x + y), Q.integer(x)) is None

    assert satask(Q.integer(x + y), Q.integer(x) & ~Q.integer(y)) is False
    assert satask(Q.integer(x + y + z), Q.integer(x) & Q.integer(y) &
        ~Q.integer(z)) is False
    assert satask(Q.integer(x + y + z), Q.integer(x) & ~Q.integer(y) &
        ~Q.integer(z)) is None
    assert satask(Q.integer(x + y + z), Q.integer(x) & ~Q.integer(y)) is None
    assert satask(Q.integer(x + y), Q.integer(x) & Q.irrational(y)) is False

    assert satask(Q.integer(x*y), Q.integer(x) & Q.integer(y)) is True
    assert satask(Q.integer(x*y), Q.integer(x)) is None

    assert satask(Q.integer(x*y), Q.integer(x) & ~Q.integer(y)) is None
    assert satask(Q.integer(x*y), Q.integer(x) & ~Q.rational(y)) is False
    assert satask(Q.integer(x*y*z), Q.integer(x) & Q.integer(y) &
        ~Q.rational(z)) is False
    assert satask(Q.integer(x*y*z), Q.integer(x) & ~Q.rational(y) &
        ~Q.rational(z)) is None
    assert satask(Q.integer(x*y*z), Q.integer(x) & ~Q.rational(y)) is None
    assert satask(Q.integer(x*y), Q.integer(x) & Q.irrational(y)) is False

