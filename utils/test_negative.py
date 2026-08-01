
def test_negative():
    assert ask(Q.negative(x), Q.negative(x)) is True
    assert ask(Q.negative(x), Q.positive(x)) is False
    assert ask(Q.negative(x), ~Q.real(x)) is False
    assert ask(Q.negative(x), Q.prime(x)) is False
    assert ask(Q.negative(x), ~Q.prime(x)) is None

    assert ask(Q.negative(-x), Q.positive(x)) is True
    assert ask(Q.negative(-x), ~Q.positive(x)) is None
    assert ask(Q.negative(-x), Q.negative(x)) is False
    assert ask(Q.negative(-x), Q.positive(x)) is True

    assert ask(Q.negative(x - 1), Q.negative(x)) is True
    assert ask(Q.negative(x + y)) is None
    assert ask(Q.negative(x + y), Q.negative(x)) is None
    assert ask(Q.negative(x + y), Q.negative(x) & Q.negative(y)) is True
    assert ask(Q.negative(x + y), Q.negative(x) & Q.nonpositive(y)) is True
    assert ask(Q.negative(2 + I)) is False
    # although this could be False, it is representative of expressions
    # that don't evaluate to a zero with precision
    assert ask(Q.negative(cos(I)**2 + sin(I)**2 - 1)) is None
    assert ask(Q.negative(-I + I*(cos(2)**2 + sin(2)**2))) is None

    assert ask(Q.negative(x**2)) is None
    assert ask(Q.negative(x**2), Q.real(x)) is False
    assert ask(Q.negative(x**1.4), Q.real(x)) is None

    assert ask(Q.negative(x**I), Q.positive(x)) is None

    assert ask(Q.negative(x*y)) is None
    assert ask(Q.negative(x*y), Q.positive(x) & Q.positive(y)) is False
    assert ask(Q.negative(x*y), Q.positive(x) & Q.negative(y)) is True
    assert ask(Q.negative(x*y), Q.complex(x) & Q.complex(y)) is None

    assert ask(Q.negative(x**y)) is None
    assert ask(Q.negative(x**y), Q.negative(x) & Q.even(y)) is False
    assert ask(Q.negative(x**y), Q.negative(x) & Q.odd(y)) is True
    assert ask(Q.negative(x**y), Q.positive(x) & Q.integer(y)) is False

    assert ask(Q.negative(Abs(x))) is False

